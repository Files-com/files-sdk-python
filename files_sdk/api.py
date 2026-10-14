import threading
from decimal import DecimalException
from typing import Any, Callable, TypeVar
from urllib.parse import quote

import files_sdk
from files_sdk.api_client import ApiClient, unexpected_response_error
from files_sdk.context import (
    Context,
    check_delay,
    check_duration,
    check_retries,
    check_workspace,
    checked_base_url,
    checked_options,
)
from files_sdk.error import InvalidParameterError
from files_sdk.transport import Transport
from files_sdk.upload import TransferLimiter
import files_sdk.util as util

T = TypeVar("T")


class Operation:
    """One logical operation: the context it runs with, the lifetime its
    steps share, and the ApiClient that sends its requests.

    A list keeps its operation for the pages it fetches later, and an
    upload or download uses one from its first request to its last. A
    relocation to another region changes the context for the rest of the
    operation only. An Operation passed where a resource expects a client
    continues it rather than starting another.
    """

    def __init__(self, context, lifetime, options=None, *, _state=None):
        self._state = _state if _state is not None else {"context": context}
        self.lifetime = lifetime
        # The options a model built from this operation's responses
        # reports, as it always has.
        self.options = {
            name: value
            for name, value in checked_options(options).items()
            if name in files_sdk.OPTS
        }
        # Whether a request of this operation may be sent again once it may
        # have reached Files.com: None to decide by its method (only a
        # request that asks for something, such as a GET, is), True for
        # requests Files.com can receive twice without harm (replay_safe)
        # and False for one that must never be repeated (completion).
        self.replay = None
        # Whether any request of this operation has been handed to the
        # network, whether or not it was then sent: until then, nothing it
        # asked for can have happened.
        self.dispatched = False
        self.api_client = ApiClient(self)

    @classmethod
    def start(cls, scope, options=None) -> "Operation":
        """Start an operation in scope (a Client, Context or legacy scope)
        with per-call options, or continue scope if it is an Operation."""
        if isinstance(scope, Operation):
            if checked_options(options):
                raise InvalidParameterError(
                    "Options cannot change an operation that has started"
                )
            return scope
        context = scope._context_for(options)
        return cls(context, context.lifetime(options), options)

    @property
    def context(self) -> Context:
        return self._state["context"]

    def relocate(self, base_url):
        self._state["context"] = self.context.relocated(base_url)

    def require_single_completion(self):
        """Raise, before an upload sends anything, if its client's own
        Requests session would retry the request that completes it."""
        context = self.context
        if context.transport.resends(context.base_url):
            raise InvalidParameterError(
                "The http_session's adapter for {} retries requests itself, so "
                "it could send the request that completes an upload twice. "
                "Mount an adapter without retries there; the SDK retries what "
                "is safe to send again.".format(context.base_url)
            )

    def completion(self) -> "Operation":
        """This operation, for a request that finishes something and must
        not be sent again once it may have been received, such as the
        request that completes an upload."""
        return self._view(replay=False)

    def replay_safe(self) -> "Operation":
        """This operation, for requests that change nothing Files.com could
        do twice, such as asking for an upload part's URL: like a request
        that only asks for something, one is sent again after its answer
        was lost."""
        return self._view(replay=True)

    def _view(self, replay):
        view = Operation(None, self.lifetime, _state=self._state)
        view.options = self.options
        view.replay = replay
        return view

    def _context_for(self, options):
        if checked_options(options):
            raise InvalidParameterError(
                "Options cannot change an operation that has started"
            )
        return self.context

    def request(self, method, path, params=None):
        """Send one API request with this operation's principal and
        settings, through the ApiClient that MCP patches."""
        Api.warn_on_options_in_params(params)
        context = self.context
        return self.api_client.send_request(
            method,
            path,
            api_key=context.api_key,
            session_id=context.session_id,
            language=context.language,
            workspace_id=context.workspace_id,
            headers=dict(context.headers),
            params=params,
        )

    def adopt(self, obj: T) -> T:
        """obj, a model built from this operation's response, keeping this
        operation's context for its own later operations."""
        obj._context = self.context  # type: ignore[attr-defined]
        return obj

    def decode_model(self, response, model: Callable[..., T]) -> T:
        """The model built from a successful response's JSON object body."""
        return decode_record(
            response,
            response.data,
            lambda record: self.adopt(model(record, self.options)),
        )

    def decode_models(self, response, model: Callable[..., T]) -> list[T]:
        """The models built from a successful response's JSON array body."""
        if not isinstance(response.data, list):
            raise unexpected_response_error(
                response, "a list was not a JSON array"
            )

        def build(record):
            return self.adopt(model(record, self.options))

        return [
            decode_record(response, record, build) for record in response.data
        ]


def decode_record(response, record, decode):
    """Return decode(record) for one JSON object record from a successful
    response. A record of any other shape, or one with a value decode
    cannot convert, is an unexpected response rather than a caller error.
    """
    if not isinstance(record, dict):
        raise unexpected_response_error(
            response, "a record was not a JSON object"
        )
    try:
        return decode(record)
    # A malformed decimal, or a decimal list that is not a list.
    except (DecimalException, TypeError):
        raise unexpected_response_error(
            response, "a record had a malformed value"
        ) from None


def path_value(value) -> str:
    """value, a path parameter such as the id in /users/{id} or the path in
    /files/{path}, as the one segment of the request path it fills: its
    text, URL-quoted whole, so that a "/" or "?" in it stays in the segment.
    "." and "..", which a URL resolves away so that the request would name
    another path, are refused."""
    text = str(value)
    if text in (".", ".."):
        raise InvalidParameterError(
            "Bad parameter: a path parameter cannot be {!r}, which would name "
            "another path".format(text)
        )
    return quote(text, safe="")


def copy_params(params, path_values=None) -> dict[str, Any]:
    """A copy of an operation's params, with path_values (such as the id
    in /users/{id}) added, that leaves the caller's dictionary unchanged.
    Nested dictionaries and lists are copied too; streams, attachments and
    other objects are shared, not copied."""
    copied: dict[str, Any] = (
        _copied(params) if isinstance(params, dict) else {}
    )
    copied.update(path_values or {})
    return copied


def _copied(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _copied(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_copied(item) for item in value]
    return value


# The module facade.

_legacy_lock = threading.Lock()
_legacy_transport: Transport | None = None
# The budget the module-level functions' uploads share: the SDK's own, as a
# client's is.
_legacy_limiter = TransferLimiter._client_owned()


def legacy_transport() -> Transport:
    """The transport the module-level functions share, created when first
    needed and again after files_sdk.close()."""
    global _legacy_transport
    with _legacy_lock:
        if _legacy_transport is None:
            _legacy_transport = Transport()
        return _legacy_transport


def close_legacy_transport():
    global _legacy_transport
    with _legacy_lock:
        transport, _legacy_transport = _legacy_transport, None
    if transport is not None:
        transport.close()


def _legacy_setting(name, check):
    value = getattr(files_sdk, name)
    try:
        return check(value)
    except (InvalidParameterError, ValueError) as error:
        # Not the value itself, which can hold a password, as in a base_url.
        raise InvalidParameterError(
            "files_sdk.{} is not valid: {}".format(name, error)
        ) from None


def legacy_context() -> Context:
    """The module's settings, as they are now."""
    return Context(
        transport=legacy_transport(),
        base_url=_legacy_setting("base_url", checked_base_url),
        base_path=files_sdk.base_path,
        api_key=files_sdk.get_api_key() or None,
        session_id=files_sdk.session_id or None,
        workspace_id=check_workspace(files_sdk.get_workspace_id()),
        language=files_sdk.get_language() or None,
        source_ip=files_sdk.get_source_ip() or None,
        open_timeout=_legacy_setting(
            "open_timeout", lambda v: check_duration("open_timeout", v)
        ),
        read_timeout=_legacy_setting(
            "read_timeout", lambda v: check_duration("read_timeout", v)
        ),
        max_network_retries=_legacy_setting(
            "max_network_retries", check_retries
        ),
        initial_network_retry_delay=_legacy_setting(
            "initial_network_retry_delay",
            lambda v: check_delay("initial_network_retry_delay", v),
        ),
        max_network_retry_delay=_legacy_setting(
            "max_network_retry_delay",
            lambda v: check_delay("max_network_retry_delay", v),
        ),
        transfer_limiter=_legacy_limiter,
    )


class LegacyScope:
    """Where the module-level functions, and models not built by a client,
    get their context: the module's settings when an operation starts, with
    options applied. A client option sends the operation to that client."""

    def __init__(self, options=None):
        self.options = dict(options or {})

    def _context_for(self, options):
        from files_sdk.client import Client

        options = {**checked_options(self.options), **checked_options(options)}
        client = options.get("client")
        if client is not None:
            if not isinstance(client, Client):
                raise InvalidParameterError(
                    "client must be a files_sdk.Client"
                )
            return client._context_for(options)
        return legacy_context().merged(options)


LEGACY = LegacyScope()


class Api:
    """The module facade's shared ApiClient, and helpers kept for code
    written against earlier versions."""

    __singleton_instance = None

    @staticmethod
    def client() -> ApiClient:
        """The ApiClient of the module facade. Its session is the Requests
        session the module-level functions send through."""
        if not Api.__singleton_instance:
            Api.__singleton_instance = ApiClient()
        return Api.__singleton_instance

    @staticmethod
    def send_request(verb, path, params, options=None):
        """Send one request with the module facade and return it with the
        options that models built from it keep."""
        operation = Operation.start(LEGACY, options)
        return operation.request(verb, path, params), operation.options

    decode_record = staticmethod(decode_record)

    @staticmethod
    def warn_on_options_in_params(params):
        for opt in files_sdk.OPTS:
            if isinstance(params, dict) and opt in params:
                util.log_warning(
                    "{} should be in the options dictionary, not the params "
                    "dictionary. You may need to create a second dictionary "
                    "that goes after params.".format(opt)
                )

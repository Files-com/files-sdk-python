"""Request options and the configuration an operation runs with.

A Context is immutable: the principal, workspace, headers, timeouts, retry
policy and transport one operation uses. A Client has one, the module
facade builds one from the module's settings when an operation starts, and
every model and list keeps the one it came from. Per-call options derive a
new Context; nothing changes the one they started from.
"""

import dataclasses
import ipaddress
import math
from urllib.parse import urlsplit
from typing import TYPE_CHECKING, Any, Callable, Literal, Mapping, TypedDict

from files_sdk.error import InvalidParameterError
from files_sdk.lifetime import CancellationToken, Lifetime, checked_duration
from files_sdk.transport import FILES_AUTH_HEADERS, Transport

if TYPE_CHECKING:
    from files_sdk.client import Client
    from files_sdk.models.session import Session
    from files_sdk.region import RegionRelocation
    from files_sdk.adaptive import UploadTuning
    from files_sdk.upload import TransferLimiter

DEFAULT_BASE_URL = "https://app.files.com"
DEFAULT_BASE_PATH = "api/rest/v1"


class _Clear:
    """The type of CLEAR."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __repr__(self):
        return "files_sdk.CLEAR"

    def __reduce__(self):
        return "CLEAR"


CLEAR: Any = _Clear()
"""An option value that removes a setting the operation would otherwise
inherit, such as a client's API key or workspace. Leaving an option out, or
setting it to None, inherits it."""


class RequestOptions(TypedDict, total=False):
    """Options for one call, such as ``client.user.find(1, {}, options)``.

    Leave an option out, or set it to None, to inherit it from the client
    (or, for the module-level functions, from the module's settings). Set
    it to ``files_sdk.CLEAR`` to remove the inherited value instead. An API
    key given here is used instead of an inherited session, and a session
    instead of an inherited API key.
    """

    api_key: str
    session_id: str
    session: "Session"
    workspace_id: int | str
    language: str
    source_ip: str
    headers: Mapping[str, str]
    open_timeout: float
    read_timeout: float
    max_network_retries: int
    request_timeout: float
    deadline: float
    cancel_token: CancellationToken
    region_policy: Literal["automatic", "disabled"]
    client: "Client"


_OPTION_NAMES = frozenset(RequestOptions.__annotations__)
REGION_POLICIES = ("automatic", "disabled")


def checked_base_url(base_url):
    """base_url, if it is an http or https URL with a host and without a
    user name, password, query or fragment."""
    if not isinstance(base_url, str):
        raise InvalidParameterError("base_url must be a string")
    parts = urlsplit(base_url)
    try:
        parts.port
    except ValueError:
        raise InvalidParameterError("base_url has an invalid port") from None
    if (
        parts.scheme.lower() not in ("http", "https")
        or not parts.hostname
        or "@" in parts.netloc
        or parts.query
        or parts.fragment
    ):
        raise InvalidParameterError(
            "base_url must be an http or https URL with a host and without a "
            "user name, password, query or fragment, such as "
            "https://app.files.com"
        )
    return base_url


def checked_options(options) -> dict[str, Any]:
    """options as a dictionary of the options it sets, with None values
    left out. Raises InvalidParameterError for an unknown option."""
    if options is None:
        return {}
    if not isinstance(options, Mapping):
        raise InvalidParameterError(
            "options must be a dictionary, not {}".format(
                type(options).__name__
            )
        )
    unknown = sorted(
        str(name) for name in options if name not in _OPTION_NAMES
    )
    if unknown:
        raise InvalidParameterError(
            "Unknown option{}: {}. Supported options are {}.".format(
                "s" if len(unknown) > 1 else "",
                ", ".join(unknown),
                ", ".join(sorted(_OPTION_NAMES)),
            )
        )
    return {
        name: value for name, value in options.items() if value is not None
    }


def _credential(name, value):
    """A credential option: None to inherit, CLEAR to remove, or its text.
    An empty string inherits, as it always has."""
    if value is CLEAR:
        return CLEAR
    if not isinstance(value, str):
        raise InvalidParameterError("{} must be a string".format(name))
    return value or None


def _session_credential(value):
    from files_sdk.models.session import Session

    if value is CLEAR:
        return CLEAR
    if not isinstance(value, Session):
        raise InvalidParameterError("session must be a files_sdk.Session")
    if not value.id:
        raise InvalidParameterError(
            "The session option needs a session that has logged in (one "
            "with an id). Create it first, such as with "
            "files_sdk.session.create()."
        )
    return str(value.id)


def principal(api_key, session_id, session):
    """A client's (api_key, session_id), from its constructor arguments.
    Unlike per-call options, it keeps both."""
    key = None if api_key is None else _credential("api_key", api_key)
    if session is not None:
        session_id = _session_credential(session)
    elif session_id is not None:
        session_id = _credential("session_id", session_id)
    return (
        None if key is CLEAR else key,
        None if session_id is CLEAR else session_id,
    )


def _clearable_text(name, value):
    """None for CLEAR or an empty string, else the text."""
    if value is CLEAR or value == "":
        return None
    if not isinstance(value, str):
        raise InvalidParameterError("{} must be a string".format(name))
    return value


def check_workspace(value):
    if value is None or value is CLEAR or value == "":
        return None
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise InvalidParameterError("workspace_id must be an integer")
    return value


def _source_ip(value):
    value = _clearable_text("source_ip", value)
    if value is not None:
        try:
            ipaddress.ip_address(value)
        except ValueError:
            raise InvalidParameterError(
                "source_ip must be an IP address, not {!r}".format(value)
            ) from None
    return value


def check_duration(name, value):
    if value is CLEAR:
        raise InvalidParameterError("{} cannot be cleared".format(name))
    try:
        return checked_duration(name, value)
    except ValueError as error:
        raise InvalidParameterError(str(error)) from None


def check_retries(value):
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise InvalidParameterError(
            "max_network_retries must be an integer of 0 or more"
        )
    return value


def check_delay(name, value):
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        raise InvalidParameterError(
            "{} must be a number of seconds of 0 or more".format(name)
        )
    return value


def _headers(value) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, Mapping):
        raise InvalidParameterError("headers must be a dictionary")
    headers = []
    reserved = {name.lower() for name in FILES_AUTH_HEADERS}
    for name, text in value.items():
        if not isinstance(name, str) or not isinstance(text, str):
            raise InvalidParameterError(
                "header names and values must be strings"
            )
        if name.lower() in reserved:
            raise InvalidParameterError(
                "Set {} with the api_key, session_id or workspace_id option, "
                "not headers".format(name)
            )
        headers.append((name, text))
    return tuple(headers)


def _region_policy(value):
    if value not in REGION_POLICIES:
        raise InvalidParameterError(
            "region_policy must be 'automatic' or 'disabled', not {!r}".format(
                value
            )
        )
    return value


@dataclasses.dataclass(frozen=True, repr=False)
class Context:
    """The configuration of one operation. See the module docstring."""

    transport: Transport
    client: "Client | None" = None
    base_url: str = DEFAULT_BASE_URL
    base_path: str = DEFAULT_BASE_PATH
    api_key: str | None = None
    session_id: str | None = None
    workspace_id: int | str | None = None
    language: str | None = None
    source_ip: str | None = None
    headers: tuple[tuple[str, str], ...] = ()
    open_timeout: float = 30
    read_timeout: float = 80
    max_network_retries: int = 3
    initial_network_retry_delay: float = 0.1
    max_network_retry_delay: float = 2
    request_timeout: float | None = None
    max_redirects: int = 30
    region_policy: str = "automatic"
    region_handler: (
        "Callable[[RegionRelocation], bool | str | None] | None"
    ) = None
    region_development_origins: frozenset[Any] = frozenset()
    # The budget of upload parts this context's uploads share, and how they
    # adapt (None for the defaults).
    transfer_limiter: "TransferLimiter | None" = None
    upload_tuning: "UploadTuning | None" = None

    def __repr__(self):
        # Never the credentials: this can end up in logs and tables.
        return "<files_sdk context {}>".format(self.base_url)

    def _context_for(self, options) -> "Context":
        """This context with options applied, for an operation of an
        object that keeps it. A client option must name its own client."""
        client = checked_options(options).get("client")
        if client is not None and client is not self.client:
            raise InvalidParameterError(
                "The client option names a different client than the one "
                "this object belongs to. Use that client's resources instead."
            )
        return self.merged(options)

    def relocated(self, base_url) -> "Context":
        """This context sending to base_url instead."""
        return dataclasses.replace(self, base_url=base_url)

    @property
    def source_address(self):
        return None if self.source_ip is None else (self.source_ip, 0)

    def merged(self, options) -> "Context":
        """This context with options (already checked) applied."""
        options = checked_options(options)
        if not options:
            return self
        changes: dict[str, Any] = {}
        api_key, session_id = self.api_key, self.session_id
        call_key = session = None
        if "api_key" in options:
            call_key = _credential("api_key", options["api_key"])
        if "session" in options:
            session = _session_credential(options["session"])
        elif "session_id" in options:
            session = _credential("session_id", options["session_id"])
        if call_key is not None:
            api_key = None if call_key is CLEAR else call_key
        if session is not None:
            session_id = None if session is CLEAR else session
        # A key given for this call wins over any session, and a session
        # given for it wins over an inherited key.
        if call_key not in (None, CLEAR):
            session_id = None
        elif session not in (None, CLEAR):
            api_key = None
        changes["api_key"], changes["session_id"] = api_key, session_id

        if "workspace_id" in options:
            changes["workspace_id"] = check_workspace(options["workspace_id"])
        if "language" in options:
            changes["language"] = _clearable_text(
                "language", options["language"]
            )
        if "source_ip" in options:
            source_ip = _source_ip(options["source_ip"])
            if source_ip is not None and not self.transport.owned:
                raise InvalidParameterError(
                    "source_ip cannot be used with a client given its own "
                    "http_session. Bind the addresses in that session's "
                    "adapters instead."
                )
            changes["source_ip"] = source_ip
        if "headers" in options:
            value = options["headers"]
            if value is CLEAR:
                changes["headers"] = ()
            else:
                merged = dict(self.headers)
                merged.update(_headers(value))
                changes["headers"] = tuple(merged.items())
        for name in ("open_timeout", "read_timeout"):
            if name in options:
                changes[name] = check_duration(name, options[name])
        if "max_network_retries" in options:
            changes["max_network_retries"] = check_retries(
                options["max_network_retries"]
            )
        if "request_timeout" in options:
            value = options["request_timeout"]
            changes["request_timeout"] = (
                None
                if value is CLEAR
                else check_duration("request_timeout", value)
            )
        if "region_policy" in options:
            changes["region_policy"] = _region_policy(options["region_policy"])
        return dataclasses.replace(self, **changes)

    def lifetime(self, options) -> Lifetime:
        """A new lifetime, starting now, for an operation with options."""
        options = checked_options(options)
        token = options.get("cancel_token")
        if token is not None and not isinstance(token, CancellationToken):
            raise InvalidParameterError(
                "cancel_token must be a files_sdk.CancellationToken"
            )
        deadline = options.get("deadline")
        if deadline is not None and (
            isinstance(deadline, bool)
            or not isinstance(deadline, (int, float))
            or not math.isfinite(deadline)
        ):
            raise InvalidParameterError(
                "deadline must be a time.monotonic() value"
            )
        return Lifetime.start(
            self.transport.closing, token, self.request_timeout, deadline
        )

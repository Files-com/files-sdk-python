import logging
import platform
import re
import sys
import time
from decimal import Decimal
from typing import Any, cast
from urllib.parse import urljoin, urlsplit

import requests

import files_sdk
import files_sdk.error
from files_sdk.attachment import AttachmentBody, has_attachment
from files_sdk.error import (
    APIConnectionError,
    APIError,
    AuthenticationError,
    InvalidRequestError,
)
import files_sdk.region as region
from files_sdk.transport import FILES_AUTH_HEADERS, url_origin
import files_sdk.util as util
from files_sdk.writing import write_all

__all__ = ["ApiClient", "ApiResponse", "FILES_AUTH_HEADERS"]

# Transfer requests get Requests' usual headers with the SDK's user agent,
# but nothing from the session: no cookies, authentication or extra headers.
_TRANSFER_HEADERS = {
    name: value
    for name, value in requests.utils.default_headers().items()
    if name != "User-Agent"
}

# The comment the SDK's own User-Agent ends with: what the process runs on,
# coarsely, and nothing about its host.
_METADATA_COMMENT = " (files-sdk-meta/1; os={os}; runtime={runtime})"
_MAX_METADATA_BYTES = 128  # The comment, with the space before it.
_MAX_USER_AGENT_BYTES = 190  # The whole value, with the comment.
# The operating systems sys.platform names exactly. FreeBSD's names also
# carry its major version.
_OPERATING_SYSTEMS = {
    "win32": "windows",
    "darwin": "macos",
    "linux": "linux",
    "android": "android",
    "ios": "ios",
}
# A Python version the comment can carry as it is.
_PYTHON_VERSION = re.compile(r"[0-9][A-Za-z0-9._+-]{0,47}")


def _operating_system():
    """The coarse operating system of this process, from sys.platform
    alone: nothing of the host's name, version or architecture."""
    name = sys.platform
    if not name:
        return "unknown"
    if name == "linux" and hasattr(sys, "getandroidapilevel"):
        return "android"  # Before Python 3.13, Android's platform is linux.
    if name.startswith("freebsd"):
        return "freebsd"
    return _OPERATING_SYSTEMS.get(name, "other")


def _python_version():
    """platform.python_version() as it is, or None if it cannot be had or
    is not a version the comment can carry."""
    try:
        version = platform.python_version()
        return version if _PYTHON_VERSION.fullmatch(version) else None
    except Exception:  # Optional metadata never stops a request.
        return None


def _default_user_agent():
    """The SDK's own User-Agent: "Files.com Python SDK v" and
    files_sdk.version as it is now, then a comment with the operating system
    and Python version. The Python version is left out when it cannot be
    had, or would make the value too long, and then the whole comment if
    the value would still be too long; the SDK's name and version are never
    cut. A name and version that are not ASCII are sent alone, as before."""
    identity = "Files.com Python SDK v{version}".format(
        version=files_sdk.version
    )
    if not identity.isascii():
        return identity
    os_name = _operating_system()
    version = _python_version()
    runtimes = ["python"]
    if version is not None:
        runtimes.insert(0, "python/" + version)
    for runtime in runtimes:
        # All ASCII, so its length is its size in bytes.
        comment = _METADATA_COMMENT.format(os=os_name, runtime=runtime)
        if (
            len(comment) <= _MAX_METADATA_BYTES
            and len(identity) + len(comment) <= _MAX_USER_AGENT_BYTES
        ):
            return identity + comment
    return identity


# The storage service's 429, 503 and 504 answers may say, in whole or
# decimal seconds, how long to wait.
_RETRY_AFTER = re.compile(r"\s*(\d+(?:\.\d+)?)\s*")

MAX_RETRY_AFTER = 60.0
"""The most seconds a storage service's Retry-After is waited for, at a
time. A longer wait, or one too long for a number, is shortened to this:
the answer is storage's to give, never the length of time the SDK blocks
for. The waits of a request's retries are still bounded by its
max_network_retries, and by the operation's deadline."""

# Transfer retries after anything but a 429 or 503 wait this long.
_TRANSFER_RETRY_DELAY = 0.1

# Requests' errors that retrying cannot fix: a URL it cannot use, a
# certificate that failed verification, a redirect loop, content it cannot
# decode, or a malformed request.
_PERMANENT_ERRORS = (
    requests.exceptions.SSLError,
    requests.exceptions.TooManyRedirects,
    requests.exceptions.InvalidURL,
    requests.exceptions.MissingSchema,
    requests.exceptions.InvalidSchema,
    requests.exceptions.URLRequired,
    requests.exceptions.InvalidHeader,
    requests.exceptions.InvalidJSONError,
    requests.exceptions.ContentDecodingError,
)

# Chunks of a streamed body logged at DEBUG are at most this long.
_DEBUG_CHUNK = 64 * 1024


def _error_detail(body):
    """The first entry of a structured error's "error" or "errors" member,
    as a dictionary."""
    detail = body["error"] if "error" in body else body.get("errors")
    if isinstance(detail, list):
        detail = detail[0] if detail else None
    if isinstance(detail, str):
        detail = {"message": detail}
    return detail if isinstance(detail, dict) else {}


def _api_error_class(error_type):
    """The APIError subclass for a Files.com error type such as
    "not-authenticated/invalid-session", or APIError when the SDK has none."""
    if not isinstance(error_type, str):
        return APIError
    name = error_type.split("/")[-1]
    class_name = (
        "".join(part.capitalize() for part in name.split("-")) + "Error"
    )
    error_class = getattr(files_sdk.error, class_name, None)
    if isinstance(error_class, type) and issubclass(error_class, APIError):
        return error_class
    return APIError


def _error_message(body, detail):
    """The message to show and log for a structured error. It comes from
    the error detail or the title, with URL credentials redacted."""
    for text in (detail.get("message"), body.get("title")):
        if isinstance(text, str) and text.strip():
            return _redact_url_credentials(text)
    return "Unknown error"


# A URL carries credentials in its userinfo ("user:password@") and, for
# signed transfer URLs, in its query string. API error text can echo either.
# A URL's host and path end where another URL begins, so URLs quoted back to
# back ('https://a/x','https://user:pw@b/y') are each redacted. Its query and
# fragment run to whitespace and are redacted whole, URLs inside them too.
_URL = re.compile(
    r"(https?://)"
    r"([^\s/?#]*@)?"
    r"((?:(?!https?://)[^\s?#])*)"
    r"([?#]\S*)?",
    re.IGNORECASE,
)


def _redact_url_credentials(text):
    def redact(url):
        scheme, userinfo, host_and_path, query = url.groups()
        return "".join(
            (
                scheme,
                "[redacted]@" if userinfo else "",
                host_and_path,
                "?[redacted]" if query else "",
            )
        )

    return _URL.sub(redact, text)


def unexpected_response_error(response, problem=None):
    """The APIConnectionError for a response that is not a usable Files.com
    API response. It keeps the status and headers, never the body. For a
    request that may have changed something and so is not sent again (see
    ApiClient._execute), such an answer, whatever its status, means it may
    have taken effect, which remote_outcome_unknown says."""
    outcome_unknown = getattr(response, "files_not_replayed", False)
    message = "Received an unexpected response from the Files.com API"
    if problem:
        message += ": " + problem
    if outcome_unknown:
        message += ". The request it answered may have taken effect, so check before repeating it"
    message += (
        ". If this problem persists, check Files.com's service status at "
        "https://status.files.com, or contact your primary account "
        "representative."
    )
    return APIConnectionError(
        message,
        http_status=response.status_code,
        headers=response.headers,
        remote_outcome_unknown=outcome_unknown,
    )


class ApiResponse(requests.Response):
    """The requests.Response of an API call, with its decoded JSON body as
    data (None for 204 No Content).

    The SDK attaches data to the Response that Requests returned, so callers
    keep every Requests attribute. This class only describes that object to
    type checkers; the SDK never creates an instance of it.
    """

    data: Any


def _attach_data(response: requests.Response, data: Any) -> ApiResponse:
    api_response = cast(ApiResponse, response)
    api_response.data = data
    return api_response


def _serialize_value(value):
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {k: _serialize_value(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_serialize_value(v) for v in value]
    return value


def _discard(response):
    """Close a response the SDK will not read to its end. Its connection is
    closed rather than reused."""
    if response.raw is not None:
        response.close()


def _retry_after(response):
    """The seconds a storage service's throttling answer (429, 503 or 504)
    asks for in its Retry-After, at most MAX_RETRY_AFTER, or None.
    Transfers alone use it."""
    if response.status_code not in (429, 503, 504):
        return None
    match = _RETRY_AFTER.fullmatch(response.headers.get("Retry-After") or "")
    if not match:
        return None
    # A value too long for a float is infinite, which min() also bounds.
    return min(float(match.group(1)), MAX_RETRY_AFTER)


# What storage services say, in their XML error, when a signed URL has
# expired: AWS ("Request has expired"), AWS and Google (ExpiredToken) and Azure.
_EXPIRED_MARKERS = (
    b"request has expired",
    b"<code>expiredtoken</code>",
    b"signature not valid in the specified time frame",
)


def _storage_says_expired(response):
    """Whether a storage refusal says the signed URL it was sent to has
    expired. Only this answer is kept, never the body."""
    if response.status_code not in (400, 403):
        return False
    body = (response.content or b"")[:4096].lower()
    return any(marker in body for marker in _EXPIRED_MARKERS)


def _for_transfer(error, subject):
    """error, raised for storage's answer to a transfer, with what the
    transfer was for, such as "the download of reports/q3.csv", added to
    its message once. Its message says nothing of the transfer URL or of
    what storage answered, so the caller's own path is all that names the
    file. Returns error, of its own class and with all it holds."""
    if getattr(error, "files_transfer_subject", None) is None:
        error.files_transfer_subject = subject
        error._message = "{} for {}".format(
            error._message or "Transfer request failed", subject
        )
        error.args = (error._message,)
    return error


def _retryable_status(status):
    return status == 429 or (status >= 500 and status != 501)


# Methods of requests that only ask Files.com for something: one of these is
# sent again after it may have been received. A request of another method may
# have changed something, so once it may have reached Files.com it is sent
# again only if its operation says that is harmless (Operation.replay_safe).
_ASKING_METHODS = frozenset({"GET", "HEAD", "OPTIONS"})

# Files.com answers a request with this error, before carrying any of it out,
# while its site is disabled. No other error answer shows that a request that
# may change something was not carried out: the same statuses, types and
# bodies, 429 and 503 included, can come after Files.com did all or part of
# it, so such a request is never sent again because of an answer.
_SITE_DISABLED = "service-unavailable/site-disabled"

# What a caller should do about a request that may have changed something and
# was not sent again, whether its answer was lost or was an error.
_CHECK_BEFORE_REPEATING = "Check whether it took effect before repeating it."
# The note on an error answering such a request.
_UNCERTAIN_ANSWER = (
    "Files.com answered with an error, but what the request asked for may "
    "still have happened, in whole or in part, so it was not sent again "
    "after this answer (remote_outcome_unknown is True). "
    + _CHECK_BEFORE_REPEATING
)


def _not_carried_out(response):
    """Whether response shows the request it answers was not carried out:
    Files.com's site-disabled error, exactly as it sends it."""
    body = response.data
    return (
        response.status_code == 422
        and isinstance(body, dict)
        and body.get("type") == _SITE_DISABLED
        and type(body.get("http-code")) is int
        and body["http-code"] == 422
    )


class _Failure(Exception):
    """One attempt's failure: the SDK error to raise if it is not retried,
    whether retrying could help, and why, for the retry log."""

    def __init__(self, error, retryable, reason, sent=True):
        super().__init__(reason)
        self.error = error
        self.retryable = retryable
        self.reason = reason
        self.sent = sent


class _RetryDeclined(Exception):
    """Raised by a transfer's build(), as a retry is about to be built, to
    not send it after all, such as once its signed URL has expired: the
    request ends with the error of the attempt before, with note added."""

    def __init__(self, note):
        super().__init__(note)
        self.note = note


class _CallerError(Exception):
    """An exception of the caller's own, such as from the stream a download
    writes to or its progress callback, carried unchanged through a request:
    never retried or taken for the request's failure, even once the
    operation has stopped."""

    def __init__(self, error):
        super().__init__(error)
        self.error = error


class ApiClient:
    """Sends the requests of one operation.

    Every model, list and resource operation builds one for its Operation,
    which holds the context (principal, settings, transport) and lifetime.
    send_request and request_headers keep the signatures that the Files.com
    MCP server patches. ApiClient() on its own sends through the module
    facade with the module's settings, as it always has.
    """

    def __init__(self, operation=None):
        self._operation = operation

    def _current(self):
        if self._operation is not None:
            return self._operation
        from files_sdk.api import LEGACY, Operation

        return Operation.start(LEGACY)

    @property
    def session(self) -> requests.Session:
        """The Requests session this client's requests go through."""
        if self._operation is not None:
            return self._operation.context.transport.session
        from files_sdk.api import legacy_transport

        return legacy_transport().session

    def send_remote_request(
        self,
        method,
        url,
        headers=None,
        body=None,
        *,
        may_retry=None,
        on_attempt=None,
        on_outcome=None,
        on_send=None,
        on_headers=None,
        on_abandon=None,
    ):
        """Send a request to a signed transfer URL, such as one part of an
        upload, and return the response. may_retry, if given, says whether
        a failed attempt may be sent again. on_attempt is called as each
        attempt starts, and on_outcome as it ends, with its HTTP status (None
        without a response) and the Retry-After seconds it asked for.
        on_send, if given, is called as each attempt goes to the network,
        once its request is built and logged; on_headers as its response's
        headers arrive, with its status and the Retry-After seconds they ask
        for, before its body is read, so they count even if the body then
        fails. on_abandon, if given, is called instead of on_outcome for an
        attempt that ended because the operation stopped (cancelled, closed
        or out of time), which says nothing about the network."""
        operation = self._current()

        def build():
            if on_attempt is not None:
                on_attempt()
            return requests.Request(
                method, url, headers=self._transfer_headers(headers), data=body
            )

        return self._execute(
            operation,
            build,
            transfer=True,
            may_retry=may_retry,
            observe=on_outcome,
            on_send=on_send,
            on_headers=on_headers,
            on_abandon=on_abandon,
        )

    def send_request(
        self,
        method,
        path,
        api_key=None,
        session_id=None,
        language=None,
        workspace_id=None,
        headers=None,
        params=None,
    ):
        operation = self._current()
        context = operation.context
        if api_key is None and session_id is None:
            api_key, session_id = context.api_key, context.session_id
        if api_key:
            session_id = None
        if language is None:
            language = context.language
        if workspace_id is None:
            workspace_id = context.workspace_id
        if headers is None:
            headers = dict(context.headers)

        if session_id:
            self.check_session_id(session_id)
        elif not path.startswith("/sessions"):
            self.check_api_key(api_key)

        headers = {
            **headers,
            **self.request_headers(
                api_key, session_id, language, workspace_id
            ),
        }

        data = None
        query_params = None
        body = None
        if params:
            if method in ["GET", "HEAD", "DELETE"]:
                _params = {}
                for k, v in params.items():
                    if isinstance(v, dict):
                        for k2, v2 in v.items():
                            _params[f"{k}[{k2}]"] = _serialize_value(v2)
                    elif isinstance(v, list):
                        # The API reads a repeated name as its last value;
                        # name[] repeated is an array. A name the caller
                        # already wrote as name[] is kept as it is.
                        name = k if k.endswith("[]") else f"{k}[]"
                        _params[name] = _serialize_value(v)
                    else:
                        _params[k] = _serialize_value(v)
                query_params = _params
            elif has_attachment(params):
                # Opens the attachments, or raises, before anything is sent.
                lifetime = operation.lifetime
                body = AttachmentBody(
                    _serialize_value(params),
                    check=lambda: lifetime.check("attachment"),
                )
                headers["Content-Type"] = body.content_type
            else:
                data = _serialize_value(params)

        def build():
            return requests.Request(
                method,
                url=urljoin(
                    operation.context.base_url,
                    operation.context.base_path + path,
                ),
                headers=headers,
                params=query_params,
                json=data,
                data=body,
            )

        if body is None:
            response = self._execute(operation, build)
        else:
            with body:
                response = self._execute(operation, build, rewind=body.seek)

        if response.status_code == 204:
            return _attach_data(response, None)
        try:
            return _attach_data(response, response.json())
        except ValueError:
            raise unexpected_response_error(response) from None

    def stream_download(self, uri, io, is_string_io=False):
        """Write the content at a signed download URL to io, as text if
        is_string_io, every byte exactly (see files_sdk.writing). A failure
        before io has taken anything is retried."""
        operation = self._current()
        lifetime = operation.lifetime
        written = False

        def check():
            lifetime.check("download")

        def took(count):
            nonlocal written
            written = True

        def write(piece):
            try:
                return io.write(piece)
            except Exception as error:
                # The caller's stream failed, not the download: carried
                # unchanged, never retried as a network failure.
                raise _CallerError(error) from None

        def consume(response):
            if response.status_code >= 400:
                response.content  # The error, for handle_error_response.
                return
            if response.status_code != 200:
                # Part of the file, or none, where all of it was asked for.
                raise APIConnectionError(
                    "Received an unusable response from file storage: a "
                    "download of the whole file was answered with HTTP "
                    "{}".format(response.status_code),
                    http_status=response.status_code,
                )
            offset = 0
            for chunk in response.iter_content(
                chunk_size=8192, decode_unicode=is_string_io
            ):
                lifetime.check("download")
                if util.enabled(logging.DEBUG):
                    util.log_debug("Download body", offset=offset, data=chunk)
                write_all(io, chunk, check, took, write)
                offset += len(chunk)

        def build():
            return requests.Request(
                "GET", uri, headers=self._transfer_headers()
            )

        try:
            self._execute(
                operation,
                build,
                transfer=True,
                consume=consume,
                may_retry=lambda: not written,
            )
        except _CallerError as failure:
            raise failure.error from None

    def _transfer_headers(self, headers=None):
        user_agent = _default_user_agent()
        return {
            **_TRANSFER_HEADERS,
            "User-Agent": user_agent,
            **(headers or {}),
        }

    def _execute(
        self,
        operation,
        build,
        *,
        transfer=False,
        consume=None,
        rewind=None,
        may_retry=None,
        observe=None,
        on_send=None,
        on_headers=None,
        on_abandon=None,
    ):
        """Send build()'s request, with the retries its failures allow, and
        return the successful response, its body read. For an API request,
        follow one regional relocation. Raise the SDK error otherwise.
        observe, if given, hears each attempt's status and Retry-After, or
        on_abandon, if given, that an attempt stopped with the operation;
        on_send and on_headers, see send_remote_request. A transfer's build()
        may decline a retry with _RetryDeclined."""
        lifetime = operation.lifetime
        retries = 0
        attempt = 0
        # The failure, or error response, a retry follows.
        previous: _Failure | requests.Response | None = None
        while True:
            context = operation.context
            if attempt and rewind is not None:
                rewind(0)
            try:
                request = build()
            except _RetryDeclined as declined:
                # Only a retry is declined, so an attempt came before it.
                if isinstance(previous, _Failure):
                    previous.error.add_note(declined.note)
                    raise previous.error from None
                assert previous is not None
                self.handle_error_response(
                    previous,
                    is_transfer=transfer,
                    note=declined.note,
                    context=context,
                )
            if transfer:
                self._check_transfer_url(context, request.url)
            # A transfer's caller decides with may_retry: sending a part or a
            # range again is how transfers recover.
            replayable = transfer or (
                operation.replay
                if operation.replay is not None
                else request.method.upper() in _ASKING_METHODS
            )
            self.log_request(request, retries, transfer)
            started = time.monotonic()
            try:
                response = self._attempt(
                    operation, request, transfer, consume, on_send, on_headers
                )
            except _Failure as failure:
                if failure.reason == "stopped" and on_abandon is not None:
                    on_abandon()
                elif observe is not None:
                    observe(None, None)
                self.log_response_error(request, started, failure.error)
                if (
                    failure.retryable
                    and retries < context.max_network_retries
                    and (not failure.sent or replayable)
                    and (may_retry is None or may_retry())
                ):
                    delay = self._retry_delay(context, retries, None, transfer)
                    self._wait_to_retry(
                        lifetime, retries, failure.reason, delay
                    )
                    previous = failure
                    retries += 1
                    attempt += 1
                    continue
                if failure.retryable and failure.sent and not replayable:
                    raise self._uncertain_outcome(context) from None
                raise failure.error from None
            attempt += 1
            if not replayable:
                # For unexpected_response_error, however this answer is used.
                response.files_not_replayed = True  # type: ignore[attr-defined]
            status = response.status_code
            if observe is not None:
                observe(status, _retry_after(response))
            self.log_response(request, started, status, response, transfer)
            if status < 400:
                return response

            if (
                not transfer
                and status == 403
                and self._relocate(operation, response, retries)
            ):
                # Moving to the site's host is one of the request's retries.
                retries += 1
                continue
            if (
                _retryable_status(status)
                and replayable
                and retries < context.max_network_retries
                and (may_retry is None or may_retry())
            ):
                delay = self._retry_delay(context, retries, response, transfer)
                self._wait_to_retry(
                    lifetime, retries, "HTTP {}".format(status), delay
                )
                previous = response
                retries += 1
                continue
            self.handle_error_response(
                response, is_transfer=transfer, context=context
            )

    def _attempt(
        self,
        operation,
        request,
        transfer,
        consume,
        on_send=None,
        on_headers=None,
    ):
        """One attempt: send request, follow its redirects and read the
        response. Returns the response or raises _Failure. on_send, if
        given, is called just before it is sent, and on_headers once the
        response's headers have arrived, with its status and Retry-After,
        before its body is read."""
        context = operation.context
        lifetime = operation.lifetime
        transport = context.transport
        with transport.exchange(lifetime, context.source_address) as exchange:
            response = None
            try:
                if on_send is not None:
                    on_send()
                response = transport.send(
                    exchange,
                    request,
                    lifetime=lifetime,
                    open_timeout=context.open_timeout,
                    read_timeout=context.read_timeout,
                    max_redirects=context.max_redirects,
                    api_origin=(
                        None if transfer else url_origin(context.base_url)
                    ),
                )
                if on_headers is not None:
                    on_headers(response.status_code, _retry_after(response))
                if consume is None:
                    response.content
                else:
                    consume(response)
            except InvalidRequestError:
                # A problem with the request itself, such as an attachment
                # stream that ended early, which sending it again cannot fix.
                if response is not None:
                    _discard(response)
                raise
            except _CallerError:
                # The caller's own exception, which stays theirs even when it
                # comes after the operation stopped, such as a callback that
                # cancels the operation and then raises.
                if response is not None:
                    _discard(response)
                raise
            except Exception as error:
                if response is not None:
                    _discard(response)
                raise self._failure(
                    operation, exchange, error, transfer
                ) from error
            except BaseException:
                if response is not None:
                    _discard(response)
                raise
            finally:
                if exchange.dispatched:
                    # See Operation.dispatched.
                    operation.dispatched = True
            if not exchange.finish():
                # The operation stopped before the response was complete.
                # An interrupted owned connection may have cut it short; a
                # session the SDK cannot interrupt may have finished it after
                # the stop, in which case it stays on the error, unused.
                error = lifetime.stopped_error(
                    "response", remote_outcome_unknown=True
                )
                if not exchange.interrupted:
                    error.response = response
                raise _Failure(error, retryable=False, reason="stopped")
            if not transfer:
                response.files_trusted_issuer = self._trusted_issuer(  # type: ignore[attr-defined]
                    context, exchange, response
                )
            return response

    @staticmethod
    def _check_transfer_url(context, url):
        """Raise, before anything is sent, unless url, a transfer URL
        Files.com named, is at least as protected as the API it came from:
        an API reached over HTTPS names only https:// transfer URLs. A
        plain http:// URL would send a file's bytes, and the signed URL
        itself, where anyone on the way could read or change them. An API
        reached over plain HTTP, as a local development server is, may name
        either."""
        if url_origin(context.base_url)[0] != "https":
            return
        if urlsplit(url).scheme.lower() != "https":
            raise APIConnectionError(
                "Files.com named a transfer URL that is not https://, while "
                "the API is reached over HTTPS, so nothing was sent to it. "
                "If this persists, contact Files.com support."
            )

    @staticmethod
    def _trusted_issuer(context, exchange, response):
        """Whether response came straight from context's API origin over
        HTTPS with certificate verification, so it may relocate the
        operation."""
        url = response.url
        return bool(
            url
            and exchange.verified
            and not exchange.left_origin
            and url_origin(url) == url_origin(context.base_url)
        )

    def _failure(self, operation, exchange, error, transfer):
        lifetime = operation.lifetime
        sent = exchange.may_have_sent(error)
        stopped = (
            exchange.interrupted
            or lifetime.stopped
            or (
                isinstance(error, requests.exceptions.Timeout)
                and exchange.deadline_bound
            )
        )
        if stopped:
            phase = "response" if sent else "request"
            return _Failure(
                lifetime.stopped_error(phase, remote_outcome_unknown=sent),
                retryable=False,
                reason="stopped",
            )
        if isinstance(error, files_sdk.error.Error):
            return _Failure(
                error, retryable=False, reason=type(error).__name__
            )
        if isinstance(error, requests.exceptions.RequestException):
            return _Failure(
                self.handle_network_error(
                    error,
                    None,
                    0,
                    base_url=None if transfer else operation.context.base_url,
                    sent=sent,
                ),
                retryable=not isinstance(error, _PERMANENT_ERRORS),
                reason=type(error).__name__,
                sent=sent,
            )
        raise error

    def _relocate(self, operation, response, retries):
        """Move the rest of operation to the host a region mismatch names,
        if this is the first such answer, the request has a retry left and
        the policy allows it. Without a retry left, raise the mismatch
        error, saying why the named host was not tried."""
        if operation._state.get("relocated"):
            return False
        try:
            body = response.json()
        except ValueError:
            # Of answers that are not JSON, only the plain-text mismatch.
            if not region.is_plain_mismatch(response):
                return False
            body = None
        response = _attach_data(response, body)
        context = operation.context
        if not region.is_mismatch(response):
            return False
        if retries >= context.max_network_retries:
            if context.region_policy == "automatic":
                self.handle_error_response(
                    response,
                    context=context,
                    note="The SDK did not send the request to the host Files.com "
                    "named, because max_network_retries allowed no more "
                    "attempts.",
                )
            return False
        base_url = region.relocation(
            operation.context,
            response,
            trusted_issuer=getattr(response, "files_trusted_issuer", False),
        )
        if base_url is None:
            return False
        operation._state["relocated"] = True
        util.log_info(
            "Region relocation",
            attempt=retries + 2,
            original_origin=region.origin_of(operation.context.base_url),
            target_origin=region.origin_of(base_url),
        )
        operation.relocate(base_url)
        return True

    @staticmethod
    def _retry_delay(context, retries, response, transfer):
        """Seconds to wait before retry number retries + 1."""
        if not transfer:
            return min(
                context.initial_network_retry_delay * 2**retries,
                context.max_network_retry_delay,
            )
        if response is not None and response.status_code in (429, 503):
            return _retry_after(response) or 0
        return _TRANSFER_RETRY_DELAY

    @staticmethod
    def _wait_to_retry(lifetime, retries, reason, delay):
        util.log_info(
            "Retrying request", attempt=retries + 2, reason=reason, wait=delay
        )
        lifetime.sleep(delay, "retry wait")

    @staticmethod
    def _adapter_caveat(context):
        """What to add when the SDK did not send a request again but the
        http_session's own adapter could have."""
        if context is not None and context.transport.resends(context.base_url):
            return (
                " The http_session's adapter retries requests itself, so it "
                "may have sent the request again."
            )
        return ""

    @classmethod
    def _uncertain_outcome(cls, context):
        message = (
            "The request may have reached Files.com, but no response "
            "arrived, so it was not sent again: what it asked for may have "
            "happened. " + _CHECK_BEFORE_REPEATING
        )
        return APIConnectionError(
            message + cls._adapter_caveat(context),
            phase="response",
            remote_outcome_unknown=True,
        )

    def request_headers(self, api_key, session_id, language, workspace_id):
        user_agent = _default_user_agent()

        headers = {
            "User-Agent": user_agent,
            "Content-Type": "application/json",
        }
        if api_key:
            headers["X-FilesAPI-Key"] = api_key
        if session_id:
            headers["X-FilesAPI-Auth"] = session_id
        if language:
            headers["Accept-Language"] = language
        if workspace_id is not None and workspace_id != "":
            headers["X-Files-Workspace-Id"] = str(workspace_id)

        return headers

    def check_api_key(self, api_key):
        if not api_key:
            raise AuthenticationError(
                "No Files.com API key provided. "
                "Pass api_key or session_id to files_sdk.Client, "
                "or call files_sdk.set_api_key(). "
                "You can generate API keys from the Files.com's web interface. "
            )

        if not api_key.isalnum():
            raise AuthenticationError(
                "Your API key is invalid (only letters and numbers are allowed)"
            )

    def check_session_id(self, session_id):
        if not session_id.isalnum():
            raise AuthenticationError(
                "The provided Session ID is invalid (only letters and numbers are allowed)"
            )

    def handle_error_response(
        self, response, is_transfer=False, *, note=None, context=None
    ):
        try:
            body = response.json()
        except ValueError:
            body = None
        response = _attach_data(response, body)

        # Only a JSON object is a structured Files.com error. Anything else,
        # such as a proxy's HTML page, means no reliable API response arrived,
        # except Files.com's plain-text region mismatch (see files_sdk.region).
        if not isinstance(response.data, dict):
            if is_transfer:
                error = APIError(
                    "Transfer request failed", http_status=response.status_code
                )
                error.files_storage_expired = _storage_says_expired(response)  # type: ignore[attr-defined]
                if note is not None:
                    error.add_note(note)
                raise error from None
            if response.data is not None or not region.is_plain_mismatch(
                response
            ):
                raise unexpected_response_error(response) from None
            # Its own text and headers, with no type or data it did not send.
            message = _redact_url_credentials(
                response.content.decode("utf-8", "replace").strip()
            )
            util.log_error(
                "API error", status=response.status_code, error_message=message
            )
            error = _api_error_class(region.MISMATCH)(
                message,
                http_body=response.content,
                headers=response.headers,
                http_status=response.status_code,
                code=response.status_code,
            )
        else:
            error = self.specific_api_error(
                response, _error_detail(response.data), is_transfer=is_transfer
            )
        # Its type says what went wrong, not whether a change was carried out.
        error.remote_outcome_unknown = getattr(
            response, "files_not_replayed", False
        ) and not _not_carried_out(response)
        error.response = response
        if error.remote_outcome_unknown:
            # The message is Files.com's, which may even say to try again.
            error.add_note(_UNCERTAIN_ANSWER + self._adapter_caveat(context))
        if note is not None:
            error.add_note(note)
        raise error from None

    def specific_api_error(self, response, error_data, is_transfer=False):
        message = (
            "Transfer request failed"
            if is_transfer
            else _error_message(response.data, error_data)
        )
        util.log_error(
            "API error", status=response.status_code, error_message=message
        )

        opts = {
            "http_body": response.content,
            "headers": response.headers,
            "http_status": response.status_code,
            "json_body": response.data,
            "code": error_data.get("code", response.status_code),
        }

        return _api_error_class(response.data.get("type"))(message, **opts)

    def handle_network_error(
        self, error, request, num_retries, *, base_url=None, sent=True
    ):
        """The APIConnectionError for a request to base_url (None for a
        transfer to file storage) that failed without a response."""
        util.log_error("Network error", error_type=type(error).__name__)
        util.log_debug("Network error details", error_message=error)
        if base_url is None:
            msg = "Could not complete a transfer to or from file storage."
        else:
            msg = (
                "Could not connect to Files.com at URL {}. Please check your "
                "internet connection and try again.".format(base_url)
            )
        msg += (
            " If this problem persists, you should check Files.com's service "
            "status at https://status.files.com, or contact your primary "
            "account representative."
        )
        if num_retries > 0:
            msg += " Request was retried {} times.".format(num_retries)
        msg += "\n\n(Network error: {})".format(type(error).__name__)

        return APIConnectionError(
            msg,
            phase="response" if sent else "request",
            remote_outcome_unknown=sent,
        )

    def log_request(self, request, num_retries, transfer=False):
        util.log_info(
            "Request", method=request.method, num_retries=num_retries
        )
        if not util.enabled(logging.DEBUG):
            return
        body = request.json if request.json is not None else request.data
        if transfer and isinstance(body, (bytes, bytearray)):
            util.log_debug(
                "Request details", url=request.url, body_length=len(body)
            )
            for offset in range(0, len(body), _DEBUG_CHUNK):
                util.log_debug(
                    "Request body",
                    offset=offset,
                    data=bytes(body[offset : offset + _DEBUG_CHUNK]),
                )
        else:
            details = {
                "url": request.url,
                "body": body,
                "query_params": request.params,
            }
            if not transfer:
                details["headers"] = dict(request.headers)
            util.log_debug("Request details", **details)

    def log_response(
        self, request, request_start, status, response, transfer=False
    ):
        util.log_info(
            "Response",
            elapsed=(time.monotonic() - request_start),
            method=request.method,
            status=status,
        )
        if util.enabled(logging.DEBUG) and not (transfer and status < 400):
            # A successful download's body was logged as it streamed.
            details = {"body": response.content}
            if not transfer:
                details["headers"] = dict(response.headers)
            util.log_debug("Response details", **details)

    def log_response_error(self, request, request_start, error):
        util.log_error(
            "Error",
            elapsed=(time.monotonic() - request_start),
            error_type=type(error).__name__,
            method=request.method,
        )
        util.log_debug("Error details", error_message=error, url=request.url)

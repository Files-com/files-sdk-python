"""File storage's status of one download request.

A response from file storage may name its download request with an X-Files-Download-Request-Id
header. The Go SDK's DownloadRequestStatus then reads that request's status with a GET of the
download URL joined with the request's ID; this module reads it the same way. The status URL
keeps the download URL's query, as the Go SDK's does, and gets the treatment of the download's
own request for the file, one bound to no version: no Files.com credentials, and the same
redirect and origin rules.

The status protocol is the one its producer implemented alongside the Go SDK's reading of it:
storage names a response with the header when it prepares a successful answer to a GET of the
file (not an error answer, and not an answer to HEAD). It answers a status request for a request
it knows with HTTP 200 and a JSON document: the request's state, "started", "completed", "failed"
or "error", and the count of bytes it read from the file's source ("bytes_transferred") in its
data, and, for a request that failed, the error that stopped it and its type at the top, beside
an http_code. It answers one for a request it does not know, or no longer does, with HTTP 404
(download_request_not_found). A status the SDK reads is one of the first kind; any other answer
is a status that could not be read.
Which storage still serves the protocol, and for how long it keeps a request's status, is
storage's: the SDK checks nothing of a status beyond its form.

A download bound to no version reads it at two points only (see files_sdk.download):
when storage answers its request for the file with an error that names the request, to explain
the error (storage that names only its successful answers gives it none), and when the file's
bytes arrive without a size to check them against, to check them against the status before they
are used. A status still "started" shows no outcome yet: it is read again, as a failed request
is retried, and without an outcome the download fails.
"""

import dataclasses
import json
import re
from urllib.parse import urlsplit, urlunsplit

import requests

from files_sdk.error import APIConnectionError, APIError

REQUEST_ID_HEADER = "X-Files-Download-Request-Id"

# An ID the SDK joins to a URL. Any other value, one with a slash, a query or
# escape character or a dot segment, would change what the URL names, so the
# SDK treats it as absent.
_REQUEST_ID = re.compile(r"[A-Za-z0-9_~-][A-Za-z0-9._~-]{0,255}")

# The most of a status document the SDK reads.
_MAX_BYTES = 64 * 1024

# An error type short and plain enough to repeat in another error's message.
_ERROR_TYPE = re.compile(r"[A-Za-z0-9_./-]{1,100}")


@dataclasses.dataclass(frozen=True)
class DownloadRequestStatus:
    """File storage's status of a download request, as storage reports it.

    status is the request's state: "started", "completed", "failed" or
    "error", as storage reports them, or None when the report names none.
    bytes_transferred is the count of bytes storage reports reading from
    the file's source for the request, or None: a count storage keeps, not
    proof of the bytes that reached this client. error is the error that
    stopped the request, with its title, type and http_code, or None: a
    status without an error explains nothing. Every value is the report's,
    never checked against the service beyond its type.
    """

    status: str | None = None
    bytes_transferred: int | None = None
    error: str | None = None
    title: str | None = None
    type: str | None = None
    http_code: int | None = None

    @property
    def failed(self) -> bool:
        """Whether the report says the request failed."""
        return self.status in ("failed", "error")

    def explanation(self) -> str:
        """The report's error, with its title, and what it says of the
        request."""
        text = self.error or ""
        if self.title:
            text = "{} - `{}`".format(self.title, text)
        said = []
        if self.status is not None:
            said.append("status {}".format(self.status))
        if self.bytes_transferred is not None:
            said.append("{} bytes transferred".format(self.bytes_transferred))
        if said:
            text = (
                "{} ({})".format(text, ", ".join(said))
                if text
                else ", ".join(said)
            )
        return text


def request_id_of(response):
    """The download request ID response names, or None."""
    value = (response.headers.get(REQUEST_ID_HEADER) or "").strip()
    return value if _REQUEST_ID.fullmatch(value) else None


def status_url(download_uri, request_id):
    """download_uri joined with request_id, as Go's url.JoinPath joins them:
    the ID becomes the path's last segment, the path is cleaned of empty and
    dot segments, and the query and fragment stay as they are."""
    parts = urlsplit(download_uri)
    path = parts.path if parts.path.startswith("/") else "/" + parts.path
    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            _clean(path + "/" + request_id),
            parts.query,
            parts.fragment,
        )
    )


def _clean(path):
    """Go's path.Clean of a path that starts with a slash: repeated slashes
    and "." segments go, and each ".." removes the segment before it."""
    kept = []
    for segment in path.split("/"):
        if segment in ("", "."):
            continue
        if segment == "..":
            if kept:
                kept.pop()
            continue
        kept.append(segment)
    return "/" + "/".join(kept)


def read(operation, download_uri, request_id):
    """File storage's status of the download request request_id of
    download_uri, read within operation. Raises an SDK error when storage
    does not answer with a status document: an error answer, such as the
    404 of a request it does not know, raises that answer's error; see
    reason for why."""
    url = status_url(download_uri, request_id)
    found = {}

    def build():
        return requests.Request(
            "GET", url, headers=operation.api_client._transfer_headers({})
        )

    def consume(response):
        if response.status_code >= 400:
            response.content  # Read for the error the answer raises.
            return
        body = bytearray()
        for chunk in response.iter_content(8192):
            body += chunk
            if len(body) > _MAX_BYTES:
                raise _unusable(
                    "it is larger than {} bytes".format(_MAX_BYTES)
                )
        if not _is_json(response):
            raise _unusable("it is not a JSON document")
        try:
            found["status"] = _decoded(bytes(body))
        except ValueError as problem:
            raise _unusable(str(problem)) from None

    try:
        operation.api_client._execute(
            operation,
            build,
            transfer=True,
            consume=consume,
            may_retry=lambda: True,
        )
    except APIError as error:
        # Storage has no status of the request to give: one it does not
        # know, or no longer does, is answered with 404.
        body = error.json_body if isinstance(error.json_body, dict) else {}
        kind = body.get("type")
        why = "HTTP {}".format(error.http_status)
        if isinstance(kind, str) and _ERROR_TYPE.fullmatch(kind):
            why += ", {}".format(kind)
        error.files_status_reason = why  # type: ignore[attr-defined]
        raise
    return found["status"]


def reason(problem):
    """Why reading a status failed with problem, briefly, for another
    error's message: storage's answer, what was wrong with its document, or
    the kind of error that stopped the request."""
    return (
        getattr(problem, "files_status_reason", None) or type(problem).__name__
    )


def _unusable(problem):
    error = APIConnectionError(
        "Received an unusable download request status from file storage: {}".format(
            problem
        )
    )
    error.files_status_reason = problem  # type: ignore[attr-defined]
    return error


def _is_json(response):
    return (
        "application/json"
        in (response.headers.get("Content-Type") or "").lower()
    )


def _decoded(body):
    """The status a document describes: its top-level type, title, error
    and http_code, and its data's status and bytes_transferred. Any other
    member, such as the request's times, is not read. The Go SDK reads the
    code as http-code, which the SDK takes too when http_code is absent.
    Raises ValueError for a document that is not a JSON object, or a value
    of the wrong type."""
    try:
        value = json.loads(body)
    except (ValueError, UnicodeDecodeError) as problem:
        raise ValueError(
            "it is not JSON ({})".format(type(problem).__name__)
        ) from None
    if not isinstance(value, dict):
        raise ValueError(
            "it is a JSON {}, not an object".format(type(value).__name__)
        )
    data = value.get("data")
    if data is None:
        data = {}
    if not isinstance(data, dict):
        raise ValueError("its data is not an object")
    bytes_transferred = data.get("bytes_transferred")
    if bytes_transferred is not None and (
        not isinstance(bytes_transferred, int)
        or isinstance(bytes_transferred, bool)
        or bytes_transferred < 0
    ):
        raise ValueError("its bytes_transferred is not a whole number")
    code = value.get("http_code")
    if code is None:
        code = value.get("http-code")
    return DownloadRequestStatus(
        status=_text(data, "status"),
        bytes_transferred=bytes_transferred,
        error=_text(value, "error"),
        title=_text(value, "title"),
        type=_text(value, "type"),
        http_code=_http_code(code),
    )


def _text(members, name):
    value = members.get(name)
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("its {} is not a string".format(name))
    return value or None


def _http_code(value):
    """The http_code, a number or, as the Go SDK also takes it, a string of
    digits; None when absent or unreadable as one."""
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, str) and value.strip().isdigit():
        return int(value)
    if value is None or isinstance(value, str):
        return None
    raise ValueError("its http_code is not a number")

"""A local stand-in for a download: Files.com's download action, which
answers with the file's signed URL, and the storage service behind it.

DownloadService serves byte ranges the way object storage does: a Range
request gets 206 with Content-Range and the file's ETag. Asked
with_download_identity, the download action binds the URL to the current
version with a download identity, as the adopted contract describes: a
token and size, and an If-Match of the version's strong ETag that storage
enforces with 412 (or, as a proxy does, a URL that storage refuses with 412
once the version is gone). Renewing with expected_download_identity gives
the same identity, or download-identity-unavailable once the version is
gone. Switches make it misbehave in the ways a download must survive or
refuse: no identity at all, ignoring ranges, compressing, answering with
the web app, expiring a URL, changing the file midway, cutting a response
short or labelling it wrongly, or weak or missing ETags.

With storage_origin set, the download URLs it hands out name that origin,
such as an Amazon S3 endpoint's, and session() gives a requests.Session
that sends what goes there to this service instead, as a name server
pointing that host here would: the SDK sees the URL Files.com gave.
bound_by_storage() does so for an S3 general-purpose endpoint, without a
download identity, as for a download storage's own answer binds.

Storage can also name its answers with a download request ID
(X-Files-Download-Request-Id) and answer that request's status at the
download URL joined with the ID, as the Go SDK's DownloadRequestStatus reads
it. By default it keeps to the status protocol's producer, as its source
builds it (historical_status): only successful answers are named, a status
is the document a test sets for its ID, and any other ID gets the producer's
404 for a request it does not know (MISSING_REQUEST). Naming error answers
too (request_id_on_errors) is a fault of the SDK's own, not the producer's.
"""

import gzip
import hashlib
import json
import os
import re
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qsl, quote, unquote, urlsplit

import requests
from requests.adapters import HTTPAdapter

from tests.upload_fixtures import SIGNED

API_PREFIX = "/api/rest/v1"
_RANGE = re.compile(r"bytes=(\d+)-(\d+)?")
IDENTITY_UNAVAILABLE = "processing-failure/download-identity-unavailable"

# An Amazon S3 general-purpose endpoint, as Files.com's S3 download URLs name.
S3_ORIGIN = "https://files-sdk-test.s3.us-east-1.amazonaws.com"


def sdk_entries(directory):
    """The private directories the SDK made in directory, for its temporary
    files, and what is in each."""
    found = []
    for name in sorted(os.listdir(directory)):
        if name.startswith(".files_sdk-"):
            found.append(name)
            found.extend(
                os.path.join(name, inner)
                for inner in sorted(os.listdir(os.path.join(directory, name)))
            )
    return found


def token_of(content):
    """The download identity token of a version with content."""
    return "v1." + hashlib.sha256(bytes(content)).hexdigest()[:24]


def _true(value):
    return value is not None and value.lower() in ("true", "1")


# The status protocol's producer answers a status request for a request it
# does not know, or no longer does, with this, and HTTP 404.
MISSING_REQUEST = {
    "type": "download_request_not_found",
    "title": None,
    "error": "Download request expired or not found. Please try this transfer again.",
    "http_code": 404,
    "errors": None,
    "data": None,
}


def historical_status(
    state,
    bytes_transferred,
    request_id="request-1",
    error=None,
    type=None,
    http_code=None,
    started_at="2026-01-01T00:00:00Z",
    completed_at=None,
):
    """A status document as the protocol's producer builds one, answered
    with HTTP 200: its error members at the top (set only for a request that
    failed), and the request in data, with no touched_at and nothing
    compacted away. How the producer encodes its times is not known, so a
    test can give them any form."""
    return {
        "type": type,
        "title": None,
        "error": error,
        "http_code": http_code,
        "errors": None,
        "data": {
            "file_download_id": 11,
            "request_id": request_id,
            "id": request_id,
            "type": "download",
            "bytes_transferred": bytes_transferred,
            "file_transfer_id": "transfer-1",
            "started_at": started_at,
            "completed_at": completed_at,
            "status": state,
            "method": "GET",
        },
    }


class DownloadService:
    """Serves one file. Replacing content, directly or through change_after,
    models the file changing between requests."""

    def __init__(self, test_case, content, reported_size=None):
        self.content = content
        self.reported_size = (
            len(content) if reported_size is None else reported_size
        )
        self.lock = threading.Lock()
        self.requests = (
            []
        )  # {"path", "range", "encoding", "issue"} in arrival order
        self.active = 0
        self.max_active = 0
        self.issued = 0  # download URLs handed out
        self.served = 0  # storage requests answered
        self.ignore_ranges = False
        self.gzip = None  # "whole": 200 answers when gzip is accepted; "ranges": range answers; "all": every answer
        self.chunked_short_once = (
            set()
        )  # range starts sent short, as a well-framed chunked body, once
        self.whole_status = None  # e.g. 206: how a request without Range is answered, with only part of the file
        self.ignore_ranges_after = (
            None  # storage requests after which Range is ignored
        )
        self.frontend = False
        self.expire_first_url = (
            None  # the first URL is refused after this many storage requests
        )
        self.refuse_all = False
        self.signed = None  # "aws", "files", "google" or "azure": URLs signed so; the first has already expired
        self.first_answer = (
            None  # (status, body) the first storage request is answered with
        )
        self.uris = []  # the download URLs handed out, in order
        self.change_after = None  # (storage requests served, new content)
        self.short_once = (
            set()
        )  # range starts cut short on their first attempt
        self.wrong_range_for = (
            set()
        )  # range starts answered with the wrong Content-Range
        self.failures = {}  # range start -> [status, times left]
        self.delay = None  # function of the range start -> seconds
        self.on_request = (
            None  # called with the Range header of each storage request
        )
        # How the download action answers with_download_identity: "if-match"
        # (an identity whose If-Match storage enforces), "proxy" (an identity
        # without headers, whose URL storage refuses once the version is
        # gone), "absent" (no identity, as an API without the contract) or
        # "unavailable" (download-identity-unavailable, as for storage that
        # cannot pin a version).
        self.identity = "if-match"
        self.tamper = (
            None  # function(identity dict, renewal) -> the identity sent
        )
        self.etag_style = (
            "strong"  # the ETag storage sends: "strong", "weak" or None
        )
        self.whole_short_once = 0  # whole responses cut short, each once
        self.negotiations = []  # the query of each download action request
        self.redirect_to = None  # an origin storage redirects each request to (its own for a same-origin redirect)
        self.overrun_once = (
            {}
        )  # range start -> extra bytes sent after the range, chunked, on its first attempt
        self.chunked = False  # send each range with chunked framing instead of a Content-Length
        self.etag_text = None  # the ETag every version shows, as origins with their own tags can
        self.ignore_if_match = (
            False  # serve whatever version there is, whatever the If-Match
        )
        self.whole_overrun_once = 0  # bytes a whole answer runs past its Content-Length (sent chunked), once
        # A threading.Event a whole answer waits for, at most 10 s, before
        # sending its last 64 KiB, so a test can observe the download while
        # the rest is held back; hold_timed_out says whether it waited in vain.
        self.hold_whole = None
        self.hold_timed_out = False
        self.request_id = None  # the download request ID storage names its successful answers with
        self.request_id_on_errors = (
            False  # whether it names its error answers too
        )
        # "full" or "short": whole answers sent chunked, with no
        # Content-Length; "short" sends half the file, still well framed.
        self.whole_unsized = None
        # Request ID -> (status, document, content type) its status answers
        # with; a document that is not bytes is sent as JSON. ("redirect",
        # URL) answers 307 to URL. A list of these answers with each in turn,
        # then keeps to the last. Any other ID gets 404 and MISSING_REQUEST.
        self.statuses = {}
        self.on_status = None  # called with each status request's headers before it is answered
        self.storage_origin = None  # the origin download URLs name, such as an S3 endpoint's; this service's own by default

        self.server = _QuietServer(("127.0.0.1", 0), self._handler())
        self.server.daemon_threads = True
        self.url = "http://127.0.0.1:{}".format(self.server.server_port)
        thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.05}
        )
        thread.start()
        test_case.addCleanup(thread.join)
        test_case.addCleanup(self.server.server_close)
        test_case.addCleanup(self.server.shutdown)

    def session(self):
        """A requests.Session that sends requests for storage_origin to this
        service, and any other as usual."""
        session = requests.Session()
        # No proxy from the environment between the client and this service.
        session.trust_env = False
        session.mount(
            self.storage_origin, _Loopback(self.storage_origin, self.url)
        )
        return session

    def bound_by_storage(self):
        """Hand out URLs of an Amazon S3 general-purpose endpoint without a
        download identity, so that a download binds itself to a version from
        storage's own first answer. Returns the session() that reaches this
        service there."""
        self.identity = "absent"
        self.storage_origin = S3_ORIGIN
        return self.session()

    @property
    def etag(self):
        if self.etag_text is not None:
            return self.etag_text
        return '"{}"'.format(hashlib.md5(self.content).hexdigest())

    def fail(
        self,
        start,
        status=503,
        times=1,
        body=b"<Error><Code>SlowDown</Code></Error>",
        retry_after=None,
        drop_body=False,
    ):
        """Answer the range starting at start with status and body, times
        times, and a Retry-After header if retry_after is given; with
        drop_body, close the connection after the headers instead of
        sending the body."""
        self.failures[start] = [status, times, body, retry_after, drop_body]

    def storage_requests(self):
        return [
            request
            for request in self.requests
            if request["path"].startswith("/storage/")
            and not request["path"].startswith("/storage/file/")
        ]

    def status_requests(self):
        return [
            request
            for request in self.requests
            if request["path"].startswith("/storage/file/")
        ]

    def named(self):
        """The header naming a storage answer's download request, if any."""
        return (
            {}
            if self.request_id is None
            else {"X-Files-Download-Request-Id": self.request_id}
        )

    def ranges(self):
        return [request["range"] for request in self.storage_requests()]

    def _handler(self):
        service = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_GET(self):
                target = urlsplit(self.path)
                with service.lock:
                    service.requests.append(
                        {
                            "at": time.monotonic(),
                            "path": target.path.replace(API_PREFIX, ""),
                            "range": self.headers.get("Range"),
                            "encoding": self.headers.get("Accept-Encoding"),
                            "issue": dict(parse_qsl(target.query)).get(
                                "issue"
                            ),
                            "query": target.query,
                            "if_match": self.headers.get("If-Match"),
                            "authorization": self.headers.get("Authorization")
                            or self.headers.get("X-FilesAPI-Key"),
                            "headers": dict(self.headers.items()),
                        }
                    )
                if target.path.startswith(API_PREFIX + "/files/"):
                    return self.download_action(target)
                if target.path.startswith("/storage/file/"):
                    return self.status(
                        unquote(target.path[len("/storage/file/") :])
                    )
                if target.path.startswith("/storage/"):
                    return self.storage(dict(parse_qsl(target.query)))
                self.answer(404, b"{}", {"Content-Type": "application/json"})

            def download_action(self, target):
                query = dict(parse_qsl(target.query))
                expected = query.get("expected_download_identity")
                wanted = (
                    _true(query.get("with_download_identity"))
                    or expected is not None
                )
                with service.lock:
                    service.negotiations.append(query)
                    content, etag = service.content, service.etag
                    unavailable = wanted and (
                        service.identity == "unavailable"
                        or (
                            expected is not None
                            and expected != token_of(content)
                        )
                    )
                    if not unavailable:
                        service.issued += 1
                    issue = service.issued
                if unavailable:
                    error = {
                        "type": IDENTITY_UNAVAILABLE,
                        "error": "Download identity unavailable",
                        "http-code": 422,
                    }
                    return self.answer(
                        422,
                        json.dumps(error).encode(),
                        {"Content-Type": "application/json"},
                    )
                remote = unquote(target.path[len(API_PREFIX + "/files/") :])
                origin = service.storage_origin or service.url
                uri = "{}/storage/file?X-Amz-Signature=secret&issue={}".format(
                    origin, issue
                )
                if service.signed is not None:
                    now = datetime.now(timezone.utc)
                    signing = (
                        SIGNED[service.signed](now - timedelta(hours=2), 60)
                        if issue == 1
                        else SIGNED[service.signed](now, 900)
                    )
                    uri = "{}/storage/file?{}&X-Amz-Signature=secret&issue={}".format(
                        origin, signing, issue
                    )
                body = {
                    "path": remote,
                    "type": "file",
                    "size": service.reported_size,
                }
                if wanted and service.identity in ("if-match", "proxy"):
                    identity = {
                        "version": 1,
                        "token": token_of(content),
                        "size": len(content),
                        "required_headers": {},
                    }
                    if service.identity == "if-match":
                        identity["required_headers"] = {"If-Match": etag}
                    else:
                        uri += "&version=" + token_of(content)
                    if service.tamper is not None:
                        identity = service.tamper(
                            identity, expected is not None
                        )
                    body["download_identity"] = identity
                body["download_uri"] = uri
                with service.lock:
                    service.uris.append(uri)
                return self.answer(
                    200,
                    json.dumps(body).encode(),
                    {"Content-Type": "application/json"},
                )

            def storage(self, query):
                with service.lock:
                    service.active += 1
                    service.max_active = max(
                        service.max_active, service.active
                    )
                    served = service.served
                    service.served += 1
                    if (
                        service.change_after
                        and service.served > service.change_after[0]
                    ):
                        service.content = service.change_after[1]
                    content, etag = service.content, service.etag
                    token = token_of(content)
                # The ETag storage sends, which may not be one a download
                # can rely on.
                sent_etag = {"strong": etag, "weak": "W/" + etag, None: None}[
                    service.etag_style
                ]
                try:
                    if (
                        service.redirect_to is not None
                        and "redirected=1" not in self.path
                    ):
                        separator = "&" if "?" in self.path else "?"
                        return self.answer(
                            307,
                            b"",
                            {
                                "Location": service.redirect_to
                                + self.path
                                + separator
                                + "redirected=1"
                            },
                        )
                    if service.on_request is not None:
                        service.on_request(self.headers.get("Range"))
                    if served == 0 and service.first_answer is not None:
                        return self.answer(*service.first_answer)
                    expired = (
                        service.expire_first_url is not None
                        and served >= service.expire_first_url
                    )
                    if service.refuse_all or (
                        expired and query.get("issue") == "1"
                    ):
                        return self.answer(
                            403,
                            b"<Error><Code>AccessDenied</Code><Message>Request has expired</Message></Error>",
                        )
                    if service.frontend:
                        return self.answer(
                            200,
                            b"<html>Files.com</html>",
                            {
                                "X-Files-Frontend-App": "true",
                                "Content-Type": "text/html",
                            },
                        )
                    if_match = self.headers.get("If-Match")
                    if service.ignore_if_match:
                        if_match = None
                    if (
                        if_match is not None and if_match != etag
                    ) or query.get("version", token) != token:
                        return self.answer(
                            412,
                            b"<Error><Code>PreconditionFailed</Code></Error>",
                        )
                    accepts_gzip = "gzip" in (
                        self.headers.get("Accept-Encoding") or ""
                    )
                    match = _RANGE.fullmatch(self.headers.get("Range") or "")
                    if match is None and service.whole_status == 206:
                        half = len(content) // 2
                        return self.answer(
                            206,
                            bytes(content[:half]),
                            tagged(
                                sent_etag,
                                {
                                    "Content-Range": "bytes 0-{}/{}".format(
                                        half - 1, len(content)
                                    )
                                },
                            ),
                        )
                    ignoring = (
                        service.ignore_ranges_after is not None
                        and served >= service.ignore_ranges_after
                    )
                    if match is None or service.ignore_ranges or ignoring:
                        body = content
                        headers = tagged(sent_etag, {})
                        if service.gzip == "all" or (
                            service.gzip == "whole" and accepts_gzip
                        ):
                            body = gzip.compress(content)
                            headers["Content-Encoding"] = "gzip"
                        if service.whole_unsized is not None:
                            sent = (
                                bytes(body)
                                if service.whole_unsized == "full"
                                else bytes(body[: len(body) // 2])
                            )
                            self.send_response(200)
                            for name, value in {
                                **headers,
                                **service.named(),
                            }.items():
                                self.send_header(name, value)
                            self.send_header("Transfer-Encoding", "chunked")
                            self.end_headers()
                            self.wfile.write(
                                (
                                    b"%x\r\n%s\r\n" % (len(sent), sent)
                                    if sent
                                    else b""
                                )
                                + b"0\r\n\r\n"
                            )
                            return None
                        with service.lock:
                            extra, service.whole_overrun_once = (
                                service.whole_overrun_once,
                                0,
                            )
                        if extra:
                            # Chunked framing wins over the Content-Length.
                            framed = bytes(body) + b"X" * extra
                            self.send_response(200)
                            for name, value in headers.items():
                                self.send_header(name, value)
                            self.send_header("Content-Length", str(len(body)))
                            self.send_header("Transfer-Encoding", "chunked")
                            self.end_headers()
                            self.wfile.write(
                                b"%x\r\n%s\r\n0\r\n\r\n"
                                % (len(framed), framed)
                            )
                            return None
                        with service.lock:
                            short = service.whole_short_once > 0
                            service.whole_short_once -= 1 if short else 0
                        if short:
                            self.send_response(200)
                            for name, value in headers.items():
                                self.send_header(name, value)
                            self.send_header("Content-Length", str(len(body)))
                            self.end_headers()
                            self.wfile.write(bytes(body[: len(body) // 2]))
                            self.close_connection = True
                            return None
                        if service.hold_whole is not None:
                            held = max(len(body) - 64 * 1024, 0)
                            try:
                                self.send_response(200)
                                for name, value in headers.items():
                                    self.send_header(name, value)
                                self.send_header(
                                    "Content-Length", str(len(body))
                                )
                                self.end_headers()
                                self.wfile.write(bytes(body[:held]))
                                self.wfile.flush()
                                if not service.hold_whole.wait(10):
                                    service.hold_timed_out = True
                                self.wfile.write(bytes(body[held:]))
                            except ConnectionError:
                                self.close_connection = (
                                    True  # The client gave up.
                                )
                            return None
                        return self.answer(200, body, headers)
                    start = int(match.group(1))
                    if start >= len(content):
                        return self.answer(
                            416,
                            b"",
                            {
                                "Content-Range": "bytes */{}".format(
                                    len(content)
                                )
                            },
                        )
                    with service.lock:
                        failure = service.failures.get(start)
                        if failure and failure[1] > 0:
                            failure[1] -= 1
                        else:
                            failure = None
                    if failure:
                        status, _times, refusal, retry_after, dropped = failure
                        headers = (
                            {}
                            if retry_after is None
                            else {"Retry-After": str(retry_after)}
                        )
                        if dropped:
                            # The headers, then nothing of the body they announce.
                            self.send_response(status)
                            for name, value in headers.items():
                                self.send_header(name, value)
                            self.send_header(
                                "Content-Length", str(len(refusal))
                            )
                            self.end_headers()
                            self.close_connection = True
                            self.connection.close()
                            return None
                        return self.answer(status, refusal, headers)
                    end = min(
                        (
                            int(match.group(2))
                            if match.group(2)
                            else len(content) - 1
                        ),
                        len(content) - 1,
                    )
                    if service.delay is not None:
                        time.sleep(service.delay(start))
                    # A view, so serving a range copies nothing in this process.
                    body = memoryview(content)[start : end + 1]
                    label = "bytes {}-{}/{}".format(start, end, len(content))
                    if start in service.wrong_range_for:
                        label = "bytes {}-{}/{}".format(
                            start + 1, end, len(content)
                        )
                    if service.gzip in ("all", "ranges"):
                        return self.answer(
                            206,
                            gzip.compress(body),
                            tagged(
                                sent_etag,
                                {
                                    "Content-Range": label,
                                    "Content-Encoding": "gzip",
                                },
                            ),
                        )
                    with service.lock:
                        extra = service.overrun_once.pop(start, 0)
                    if extra or service.chunked:
                        # Chunked, so nothing below the SDK can tell the
                        # range from one that runs long.
                        framed = bytes(body) + b"X" * extra
                        self.send_response(206)
                        self.send_header("Content-Range", label)
                        if sent_etag:
                            self.send_header("ETag", sent_etag)
                        self.send_header("Transfer-Encoding", "chunked")
                        self.end_headers()
                        try:
                            self.wfile.write(
                                b"%x\r\n%s\r\n0\r\n\r\n"
                                % (len(framed), framed)
                            )
                        except ConnectionError:
                            self.close_connection = True
                        return None
                    if start in service.chunked_short_once:
                        # Properly framed, so nothing below the SDK notices
                        # that fewer bytes came than Content-Range says.
                        service.chunked_short_once.discard(start)
                        short = bytes(body[: len(body) // 2])
                        self.send_response(206)
                        self.send_header("Content-Range", label)
                        if sent_etag:
                            self.send_header("ETag", sent_etag)
                        self.send_header("Transfer-Encoding", "chunked")
                        self.end_headers()
                        self.wfile.write(
                            b"%x\r\n%s\r\n0\r\n\r\n" % (len(short), short)
                        )
                        return None
                    if start in service.short_once:
                        service.short_once.discard(start)
                        self.send_response(206)
                        self.send_header("Content-Range", label)
                        self.send_header("Content-Length", str(len(body)))
                        if sent_etag:
                            self.send_header("ETag", sent_etag)
                        self.end_headers()
                        self.wfile.write(body[: len(body) // 2])
                        self.close_connection = True
                        return None
                    return self.answer(
                        206, body, tagged(sent_etag, {"Content-Range": label})
                    )
                finally:
                    with service.lock:
                        service.active -= 1

            def status(self, request_id):
                if service.on_status is not None:
                    service.on_status(dict(self.headers.items()))
                found = service.statuses.get(request_id)
                if isinstance(found, list):
                    with service.lock:
                        found = found.pop(0) if len(found) > 1 else found[0]
                if found is None:
                    return self.answer(
                        404,
                        json.dumps(MISSING_REQUEST).encode(),
                        {"Content-Type": "application/json"},
                    )
                if found[0] == "redirect":
                    return self.answer(307, b"", {"Location": found[1]})
                status, document, content_type = found
                body = (
                    document
                    if isinstance(document, bytes)
                    else json.dumps(document).encode()
                )
                return self.answer(
                    status, body, {"Content-Type": content_type}
                )

            def answer(self, status, body, headers=None):
                storage = self.path.startswith(
                    "/storage/"
                ) and not self.path.startswith("/storage/file/")
                if storage and (status < 400 or service.request_id_on_errors):
                    headers = {**(headers or {}), **service.named()}
                try:
                    self.send_response(status)
                    for name, value in (headers or {}).items():
                        self.send_header(name, value)
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                except ConnectionError:
                    self.close_connection = True

            def log_message(self, *args):
                pass

        return Handler


def tagged(etag, headers):
    """headers, with etag as the ETag, if there is one."""
    return {**headers, "ETag": etag} if etag else headers


class _Loopback(HTTPAdapter):
    """Sends a request for origin to local instead, with enough connections
    for the ranges of a download from S3 at once."""

    def __init__(self, origin, local):
        super().__init__(pool_maxsize=256)
        self.origin = origin
        self.local = local

    def send(self, request, *args, **kwargs):
        request.url = self.local + request.url[len(self.origin) :]
        return super().send(request, *args, **kwargs)


class _QuietServer(ThreadingHTTPServer):
    # Enough waiting connections for the ranges of a download from S3 at once.
    request_queue_size = 256

    def handle_error(self, request, client_address):
        if not isinstance(sys.exc_info()[1], ConnectionError):
            super().handle_error(request, client_address)


class TreeService:
    """Serves a tree of remote folders and files: folder listings, a page of
    page_size entries at a time, each file's download URL, and its content
    by range. files maps each file's path to its content; folders lists
    folders with nothing in them. Downloads get a download identity whose
    If-Match storage enforces, as from DownloadService, unless legacy."""

    def __init__(self, test_case, files, folders=(), page_size=2):
        self.files = dict(files)
        self.folders = set(folders)
        self.page_size = page_size
        self.lock = threading.Lock()
        self.listed = []  # (folder, cursor) of each listing page
        self.downloads = (
            []
        )  # paths whose content was fetched, in arrival order
        self.fail_paths = set()  # files whose content storage refuses
        self.refuse_listing = set()  # folders whose listing fails
        self.delay = 0.0
        self.on_download = None  # called with the path of each content request
        self.legacy = (
            False  # no download identities, as an API without the contract
        )
        self.negotiations = []  # (path, query) of each download action request
        self.active = 0  # content requests being answered now
        self.max_active = 0
        self.server = _QuietServer(("127.0.0.1", 0), self._handler())
        self.server.daemon_threads = True
        self.url = "http://127.0.0.1:{}".format(self.server.server_port)
        thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.05}
        )
        thread.start()
        test_case.addCleanup(thread.join)
        test_case.addCleanup(self.server.server_close)
        test_case.addCleanup(self.server.shutdown)

    def entries(self, folder):
        """The entries directly in folder, folders and files, by path."""
        prefix = folder + "/" if folder else ""
        found = {}
        for path in list(self.files) + list(self.folders):
            if not path.startswith(prefix):
                continue
            rest = path[len(prefix) :]
            name = rest.split("/")[0]
            full = prefix + name
            if "/" in rest or path in self.folders:
                found[full] = {"path": full, "type": "directory"}
            else:
                found[full] = {
                    "path": full,
                    "type": "file",
                    "size": len(self.files[path]),
                    "mtime": "2026-09-25T00:00:00Z",
                }
        return [found[key] for key in sorted(found)]

    def _handler(self):
        service = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_GET(self):
                target = urlsplit(self.path)
                query = dict(parse_qsl(target.query))
                if target.path.startswith(API_PREFIX + "/folders/"):
                    folder = unquote(
                        target.path[len(API_PREFIX + "/folders/") :]
                    )
                    with service.lock:
                        service.listed.append((folder, query.get("cursor")))
                    if folder in service.refuse_listing:
                        return self.json(
                            403,
                            {
                                "type": "not-authorized",
                                "error": "no",
                                "http-code": 403,
                            },
                        )
                    entries = service.entries(folder)
                    if (
                        not entries
                        and folder
                        and folder not in service.folders
                    ):
                        return self.json(
                            404,
                            {
                                "type": "not-found",
                                "error": "Folder not found",
                                "http-code": 404,
                            },
                        )
                    start = int(query.get("cursor") or 0)
                    page = entries[start : start + service.page_size]
                    headers = {}
                    if start + service.page_size < len(entries):
                        headers["X-Files-Cursor"] = str(
                            start + service.page_size
                        )
                    return self.json(200, page, headers)
                if target.path.startswith(API_PREFIX + "/files/"):
                    path = unquote(target.path[len(API_PREFIX + "/files/") :])
                    with service.lock:
                        service.negotiations.append((path, query))
                        content = service.files.get(path)
                    if content is None:
                        return self.json(
                            404,
                            {
                                "type": "not-found",
                                "error": "File not found",
                                "http-code": 404,
                            },
                        )
                    expected = query.get("expected_download_identity")
                    wanted = (
                        _true(query.get("with_download_identity"))
                        or expected is not None
                    )
                    if (
                        wanted
                        and expected is not None
                        and expected != token_of(content)
                    ):
                        return self.json(
                            422,
                            {
                                "type": IDENTITY_UNAVAILABLE,
                                "error": "Download identity unavailable",
                                "http-code": 422,
                            },
                        )
                    body = {
                        "path": path,
                        "type": "file",
                        "size": len(content),
                        "download_uri": "{}/storage/{}?X-Amz-Signature=secret".format(
                            service.url, quote(path)
                        ),
                    }
                    if wanted and not service.legacy:
                        body["download_identity"] = {
                            "version": 1,
                            "token": token_of(content),
                            "size": len(content),
                            "required_headers": {
                                "If-Match": '"{}"'.format(
                                    hashlib.md5(content).hexdigest()
                                )
                            },
                        }
                    return self.json(200, body)
                if target.path.startswith("/storage/"):
                    path = unquote(target.path[len("/storage/") :])
                    with service.lock:
                        service.downloads.append(path)
                        service.active += 1
                        service.max_active = max(
                            service.max_active, service.active
                        )
                    try:
                        return self.serve(path)
                    finally:
                        with service.lock:
                            service.active -= 1
                self.json(404, {"type": "not-found", "error": "no route"})

            def serve(self, path):
                if service.on_download is not None:
                    service.on_download(path)
                if path in service.fail_paths:
                    return self.body(500, b"<Error/>")
                time.sleep(service.delay)
                content = service.files[path]
                if_match = self.headers.get("If-Match")
                if if_match is not None and if_match != '"{}"'.format(
                    hashlib.md5(content).hexdigest()
                ):
                    return self.body(
                        412, b"<Error><Code>PreconditionFailed</Code></Error>"
                    )
                match = _RANGE.fullmatch(self.headers.get("Range") or "")
                if match is None:
                    return self.body(
                        200,
                        content,
                        {
                            "ETag": '"{}"'.format(
                                hashlib.md5(content).hexdigest()
                            )
                        },
                    )
                start = int(match.group(1))
                if start >= len(content):
                    return self.body(
                        416,
                        b"",
                        {"Content-Range": "bytes */{}".format(len(content))},
                    )
                end = min(
                    int(match.group(2) or len(content) - 1), len(content) - 1
                )
                return self.body(
                    206,
                    content[start : end + 1],
                    {
                        "Content-Range": "bytes {}-{}/{}".format(
                            start, end, len(content)
                        ),
                        "ETag": '"{}"'.format(
                            hashlib.md5(content).hexdigest()
                        ),
                    },
                )

            def json(self, status, value, headers=None):
                self.body(
                    status,
                    json.dumps(value).encode(),
                    {"Content-Type": "application/json", **(headers or {})},
                )

            def body(self, status, data, headers=None):
                try:
                    self.send_response(status)
                    for name, value in (headers or {}).items():
                        self.send_header(name, value)
                    self.send_header("Content-Length", str(len(data)))
                    self.end_headers()
                    self.wfile.write(data)
                except ConnectionError:
                    self.close_connection = True

            def log_message(self, *args):
                pass

        return Handler

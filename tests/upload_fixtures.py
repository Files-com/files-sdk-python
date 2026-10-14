"""A local stand-in for what an upload talks to: Files.com's begin_upload
and the request that completes an upload, and the storage its parts go to.

Unlike LoopbackApi, which plays back responses in order, UploadService
answers each request by what it asks for, so parts can arrive in any order,
at the same time and more than once. It keeps every attempt, so tests can
check exactly which bytes arrived for which part.
"""

import collections
import hashlib
import json
import sys
import threading
import time
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qsl, unquote, urlsplit

import requests

API_PREFIX = "/api/rest/v1"
BODY_SEND = {"partsize": "required-header Content-Length", "partdata": "body"}

# Files.com's answer while a site is disabled, as its API middleware sends it:
# the one error answer that shows a request was not carried out.
SITE_DISABLED = {
    "error": "This site is temporarily unavailable.",
    "type": "service-unavailable/site-disabled",
    "title": "Site Disabled",
    "http-code": 422,
}

# How storage services refuse a signed URL that has expired: status and body.
EXPIRED = {
    "aws": (
        403,
        b"<Error><Code>AccessDenied</Code><Message>Request has expired</Message></Error>",
    ),
    "google": (
        400,
        b"<Error><Code>ExpiredToken</Code><Message>Invalid argument.</Message></Error>",
    ),
    "azure": (
        403,
        b"<Error><Code>AuthenticationFailed</Code><AuthenticationErrorDetail>Signature not valid in the "
        b"specified time frame</AuthenticationErrorDetail></Error>",
    ),
}

# Signed URL queries that say when they expire, from a signing time and a
# lifetime in seconds.
SIGNED = {
    "aws": lambda at, seconds: "X-Amz-Date={:%Y%m%dT%H%M%SZ}&X-Amz-Expires={}".format(
        at, seconds
    ),
    "files": lambda at, seconds: "X-Files-Date={:%Y%m%dT%H%M%SZ}&X-Files-Expires={}".format(
        at, seconds
    ),
    "google": lambda at, seconds: "X-Goog-Date={:%Y%m%dT%H%M%SZ}&X-Goog-Expires={}".format(
        at, seconds
    ),
    "azure": lambda at, seconds: "sp=w&se={:%Y-%m-%dT%H:%M:%SZ}".format(
        at + timedelta(seconds=seconds)
    ),
}


class StoredPart:
    def __init__(self, number, query, headers, body, ref="upload-1"):
        self.ref = ref
        self.number = number
        self.query = query
        self.raw_query = query
        self.headers = headers
        self.body = body


class UploadService:
    """Serves uploads' API requests and parts.

    part_size is the size of every part, or a function of the part number,
    and storage_query each part URL's query, or a function of the part
    number. grant holds extra fields for every part description, such as
    {"parallel_parts": False}. With storage_origin set, part URLs name that
    origin, such as an S3 endpoint's, with one URL for every part of an
    upload, as S3 names a multipart upload's object, whose storage_query
    must number the part with partNumber; session() gives a
    requests.Session that sends what goes there to this service instead.
    initial_parts is how many parts the first begin_upload of an upload
    describes when it asks for no particular number.
    Hooks change how storage answers: fail(),
    hang_up(), hold() and expire_first(). Each upload begun gets a new
    reference (upload-1, upload-2, ...); forget() makes begin_upload answer
    404 for one, as Files.com does once an upload expires, and
    refuse_paths makes it refuse to begin uploads to those paths. A
    completed upload is a remote file, with a modification time of its own,
    that GET /files/{path} describes until replace() or remove().
    """

    def __init__(
        self,
        test_case,
        part_size=4,
        grant=None,
        storage_query="X-Amz-Signature=secret",
    ):
        self.part_size = (
            part_size if callable(part_size) else (lambda number: part_size)
        )
        self.grant = {
            "http_method": "PUT",
            "headers": {},
            "parameters": {},
            "send": BODY_SEND,
            "parallel_parts": True,
            "retry_parts": True,
            "available_parts": 10000,
            **(grant or {}),
        }
        self.storage_query = storage_query
        self.storage_origin = (
            None  # the origin part URLs name; this service's own by default
        )
        self.initial_parts = 1  # parts the first begin_upload of an upload describes, unless it asks for some
        self.lock = threading.Lock()
        self.begins = []  # begin_upload parameters, in arrival order
        self.stored = collections.defaultdict(
            list
        )  # part number -> StoredPart attempts
        self.puts = []  # part numbers, in arrival order
        self.put_times = (
            []
        )  # (time.monotonic(), part number) as each part arrives
        self.finishes = []  # completion request bodies
        self.active = 0
        self.max_active = 0
        self.issued = (
            collections.Counter()
        )  # part number -> descriptions given
        self._failures = collections.defaultdict(
            list
        )  # part -> [(status, retry_after) or "hang up"]
        self._holds = {}  # part -> (arrived, release) events
        self._expire_first = None
        self.on_put = None  # called with the part number as each part arrives
        self.slow_body = (
            0.0  # seconds a part's answer keeps its body after its headers
        )
        self.finish_status = 200
        self.finish_error = (
            None  # the body a finish_status other than 200 comes with
        )
        self.finish_hang_up = False  # read the completion, then hang up
        self.finish_body = None  # complete the upload, then answer 200 with this instead of the file (bytes as they are)
        self.uploads = 0  # uploads begun
        self.forgotten = set()  # references begin_upload no longer knows
        self.refuse_paths = set()  # destinations begin_upload refuses
        self.by_ref = collections.defaultdict(
            lambda: collections.defaultdict(list)
        )  # ref -> number -> parts
        self.folders = []  # folders created
        self.begun_paths = (
            []
        )  # (destination, ref or None) of each begin_upload
        self.api_keys = (
            []
        )  # (request path, X-FilesAPI-Key) of each API request
        self.remote = {}  # path -> {"size", "mtime"} of each remote file
        self.lookups = []  # paths GET /files/{path} described
        self.on_finish = None  # called with the path of each completion request, before it is answered
        self._versions = 0

        self.server = _QuietServer(("127.0.0.1", 0), self._handler())
        self.server.daemon_threads = True
        self.url = "http://127.0.0.1:{}".format(self.server.server_port)
        thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.005}
        )
        thread.start()
        test_case.addCleanup(thread.join)
        test_case.addCleanup(self.server.server_close)
        test_case.addCleanup(self.server.shutdown)
        test_case.addCleanup(self.release_all)

    def session(self):
        """A requests.Session that sends requests for storage_origin to this
        service, and any other as usual."""
        from tests.download_fixtures import _Loopback

        session = requests.Session()
        # No proxy from the environment between the client and this service.
        session.trust_env = False
        session.mount(
            self.storage_origin, _Loopback(self.storage_origin, self.url)
        )
        return session

    # Hooks.

    def fail(
        self,
        number,
        status=503,
        times=1,
        retry_after=None,
        body=b"<Error><Code>SlowDown</Code></Error>",
    ):
        """Answer the next times attempts at part number with status and
        body, and a Retry-After header if retry_after is given."""
        self._failures[number].extend([(status, retry_after, body)] * times)

    def hang_up(self, number, times=1):
        """Read the next times attempts at part number, then close the
        connection without answering."""
        self._failures[number].extend(["hang up"] * times)

    def drop_body(self, number, times=1, status=200, retry_after=None):
        """Answer the next times attempts at part number with status's
        headers, and a Retry-After header if retry_after is given, then
        close the connection before its body."""
        self._failures[number].extend(
            [("drop body", status, retry_after)] * times
        )

    def hold(self, number):
        """Keep part number waiting once it arrives until release(number).
        Returns an event set when it arrives."""
        arrived, release = threading.Event(), threading.Event()
        self._holds[number] = (arrived, release)
        return arrived

    def release(self, number):
        self._holds[number][1].set()

    def release_all(self):
        for _arrived, release in self._holds.values():
            release.set()

    def expire_first(self, form="expires"):
        """Describe each part the first time with a URL that has already
        expired, which storage refuses; renewed descriptions work. form is
        what says so: the description's expires time ("expires"), or only
        the signed URL's own query ("aws", "files", "google" or "azure")."""
        self._expire_first = form

    # What arrived.

    def part(self, number):
        """The bytes of part number's last attempt."""
        return self.stored[number][-1].body

    def assembled(self):
        """The file the last completion request describes: its parts, by the
        ETags it lists, in part order."""
        finish = self.finishes[-1]
        data = b""
        for tag in finish["etags"]:
            [match] = [
                part
                for part in self.stored[tag["part"]]
                if _etag(part.body) == tag["etag"]
            ][-1:]
            data += match.body
        return data

    def attempts(self, number):
        return [part.body for part in self.stored[number]]

    def forget(self, ref):
        self.forgotten.add(ref)

    def completed(self, path):
        """The content of the upload completed last to path, assembled from
        its own parts by the ETags its completion lists."""
        [finish] = [
            finish for finish in self.finishes if finish["path"] == path
        ][-1:]
        data = b""
        for tag in finish["etags"]:
            [match] = [
                part
                for part in self.by_ref[finish["ref"]][tag["part"]]
                if _etag(part.body) == tag["etag"]
            ][-1:]
            data += match.body
        return data

    def completed_paths(self):
        return [finish["path"] for finish in self.finishes]

    def _new_file(self, path, size):
        with self.lock:
            self._versions += 1
            self.remote[path] = {
                "size": size,
                "mtime": "2026-09-26T00:00:00.{:06d}Z".format(self._versions),
            }
            return dict(self.remote[path])

    def replace(self, path, size):
        """Put another file at path, as another client might."""
        self._new_file(path, size)

    def remove(self, path):
        with self.lock:
            self.remote.pop(path, None)

    # The server.

    def describe(self, ref, number):
        with self.lock:
            self.issued[number] += 1
            issue = self.issued[number]
        form = self._expire_first
        expired = form is not None and issue == 1
        now = datetime.now(timezone.utc)
        expires = now + (
            timedelta(hours=-1)
            if expired and form == "expires"
            else timedelta(minutes=15)
        )
        query = (
            self.storage_query(number)
            if callable(self.storage_query)
            else self.storage_query
        )
        if form in SIGNED:
            signed = (
                SIGNED[form](now - timedelta(hours=2), 60)
                if expired
                else SIGNED[form](now, 900)
            )
            query = "{}&{}".format(signed, query)
        if self.storage_origin is None:
            uri = "{}/storage/{}/{}?{}&issue={}".format(
                self.url, ref, number, query, issue
            )
        else:
            # As S3 names a multipart upload's object: one URL for every part,
            # which its query numbers.
            uri = "{}/storage/{}?{}&issue={}".format(
                self.storage_origin, ref, query, issue
            )
        record = {
            "ref": ref,
            "part_number": number,
            "partsize": self.part_size(number),
            "next_partsize": self.part_size(number + 1),
            "upload_uri": uri,
            "expires": expires.isoformat().replace("+00:00", "Z"),
            **self.grant,
        }
        return {
            name: value for name, value in record.items() if value is not None
        }

    def _handler(self):
        service = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"
            # Each answer's headers and body are separate writes: without
            # TCP_NODELAY, the body can wait for the client's delayed ACK of
            # the headers (40 ms on Linux), which no test asks for.
            disable_nagle_algorithm = True

            def do_POST(self):
                body = self.rfile.read(
                    int(self.headers.get("Content-Length") or 0)
                )
                params = json.loads(body) if body else {}
                path = urlsplit(self.path).path
                with service.lock:
                    service.api_keys.append(
                        (unquote(path), self.headers.get("X-FilesAPI-Key"))
                    )
                if path.startswith(API_PREFIX + "/file_actions/begin_upload/"):
                    destination = unquote(
                        path[len(API_PREFIX + "/file_actions/begin_upload/") :]
                    )
                    with service.lock:
                        service.begins.append(params)
                        service.begun_paths.append(
                            (destination, params.get("ref"))
                        )
                        if (
                            not params.get("ref")
                            and destination not in service.refuse_paths
                        ):
                            service.uploads += 1
                    if destination in service.refuse_paths:
                        return self.answer(
                            422,
                            {
                                "type": "processing-failure",
                                "error": "refused",
                                "http-code": 422,
                            },
                        )
                    if params.get("ref") in service.forgotten:
                        return self.answer(
                            404,
                            {
                                "type": "not-found",
                                "error": "Upload not found",
                                "http-code": 404,
                            },
                        )
                    first = params.get("part") or 1
                    count = params.get("parts") or (
                        1 if params.get("ref") else service.initial_parts
                    )
                    ref = params.get("ref") or "upload-{}".format(
                        service.uploads
                    )
                    self.answer(
                        200,
                        [
                            service.describe(ref, first + index)
                            for index in range(count)
                        ],
                    )
                elif path.startswith(API_PREFIX + "/folders/"):
                    remote = unquote(path[len(API_PREFIX + "/folders/") :])
                    with service.lock:
                        service.folders.append(remote)
                    self.answer(201, {"path": remote, "type": "directory"})
                elif path.startswith(API_PREFIX + "/files/"):
                    remote = unquote(path[len(API_PREFIX + "/files/") :])
                    with service.lock:
                        service.finishes.append({**params, "path": remote})
                    if service.on_finish is not None:
                        service.on_finish(remote)
                    if service.finish_hang_up:
                        self.close_connection = True
                        self.connection.close()
                    elif service.finish_body is not None:
                        service._new_file(remote, params.get("size"))
                        self.answer(200, service.finish_body)
                    elif service.finish_status != 200:
                        error = (
                            {"type": "processing-failure", "error": "busy"}
                            if service.finish_error is None
                            else service.finish_error
                        )
                        self.answer(service.finish_status, error)
                    else:
                        found = service._new_file(remote, params.get("size"))
                        self.answer(
                            200, {"path": remote, "type": "file", **found}
                        )
                else:
                    self.answer(
                        404, {"type": "not-found", "error": "no route"}
                    )

            def do_GET(self):
                path = urlsplit(self.path).path
                if not path.startswith(API_PREFIX + "/file_actions/metadata/"):
                    return self.answer(
                        404, {"type": "not-found", "error": "no route"}
                    )
                remote = unquote(
                    path[len(API_PREFIX + "/file_actions/metadata/") :]
                )
                with service.lock:
                    service.lookups.append(remote)
                    found = service.remote.get(remote)
                if found is None:
                    return self.answer(
                        404,
                        {
                            "type": "not-found",
                            "error": "File not found",
                            "http-code": 404,
                        },
                    )
                self.answer(200, {"path": remote, "type": "file", **found})

            def do_PUT(self):
                target = urlsplit(self.path)
                if target.path.count("/") == 2:
                    # An S3 object's URL, the same for every part: its query numbers the part.
                    ref, number = (
                        target.path.rsplit("/", 1)[1],
                        dict(parse_qsl(target.query))["partNumber"],
                    )
                else:
                    ref, number = target.path.rsplit("/", 2)[1:]
                number = int(number)
                with service.lock:
                    service.active += 1
                    service.max_active = max(
                        service.max_active, service.active
                    )
                # Whether this part has already stopped counting as active.
                retired = False
                try:
                    body = self.rfile.read(
                        int(self.headers.get("Content-Length") or 0)
                    )
                    query = dict(
                        parse_qsl(target.query, keep_blank_values=True)
                    )
                    part = StoredPart(
                        number, query, dict(self.headers), body, ref
                    )
                    part.raw_query = target.query
                    with service.lock:
                        service.stored[number].append(part)
                        service.by_ref[ref][number].append(part)
                        service.puts.append(number)
                        service.put_times.append((time.monotonic(), number))
                        failure = (
                            service._failures[number].pop(0)
                            if service._failures[number]
                            else None
                        )
                    if service.on_put is not None:
                        service.on_put(number)
                    if number in service._holds:
                        arrived, release = service._holds[number]
                        arrived.set()
                        release.wait(30)
                    if (
                        service._expire_first is not None
                        and query.get("issue") == "1"
                    ):
                        self.answer(
                            403,
                            b"<Error><Code>AccessDenied</Code><Message>Request has expired</Message></Error>",
                        )
                    elif failure == "hang up":
                        self.close_connection = True
                        self.connection.close()
                    elif failure is not None and failure[0] == "drop body":
                        _drop, status, retry_after = failure
                        try:
                            self.send_response(status)
                            self.send_header(
                                "ETag", '"{}"'.format(_etag(body))
                            )
                            if retry_after is not None:
                                self.send_header(
                                    "Retry-After", str(retry_after)
                                )
                            self.send_header("Content-Length", "2")
                            self.end_headers()
                        except ConnectionError:
                            pass
                        self.close_connection = True
                        self.connection.close()
                    elif failure is not None:
                        status, retry_after, refusal = failure
                        headers = (
                            {}
                            if retry_after is None
                            else {"Retry-After": str(retry_after)}
                        )
                        self.answer(status, refusal, headers)
                    elif service.slow_body:
                        self.answer(
                            200,
                            b"ok",
                            {"ETag": '"{}"'.format(_etag(body))},
                            hold_body=service.slow_body,
                        )
                    else:
                        # The empty acknowledgment the client completes the
                        # part on is sent, and the part stops counting, under
                        # the lock a new part takes to count itself: a part
                        # the client sends once it has this answer is never
                        # counted beside it.
                        headers = {"ETag": '"{}"'.format(_etag(body))}
                        with service.lock:
                            self.answer(200, b"", headers)
                            service.active -= 1
                            retired = True
                finally:
                    if not retired:
                        with service.lock:
                            service.active -= 1

            def answer(self, status, body, headers=None, hold_body=0.0):
                if not isinstance(body, bytes):
                    body = json.dumps(body).encode()
                    headers = {
                        "Content-Type": "application/json",
                        **(headers or {}),
                    }
                try:
                    self.send_response(status)
                    for name, value in (headers or {}).items():
                        self.send_header(name, value)
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    if hold_body:
                        # The headers are sent; the body comes later.
                        time.sleep(hold_body)
                    self.wfile.write(body)
                except ConnectionError:
                    self.close_connection = (
                        True  # The client stopped the part.
                    )

            def log_message(self, *args):
                pass

        return Handler


class _QuietServer(ThreadingHTTPServer):
    # Accepts a job's many simultaneous connections, which the default
    # backlog of 5 would leave waiting for the client to try again.
    request_queue_size = 256

    def handle_error(self, request, client_address):
        # A client that stopped a part mid-request resets its connection.
        if not isinstance(sys.exc_info()[1], ConnectionError):
            super().handle_error(request, client_address)


def _etag(body):
    return hashlib.md5(body).hexdigest()

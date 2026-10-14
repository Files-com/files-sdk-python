import email.parser
import email.policy
import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch
from urllib.parse import parse_qsl, urlsplit

import files_sdk

API_PREFIX = "/api/rest/v1"


class FormPart:
    def __init__(self, name, filename, content_type, data):
        self.name = name
        self.filename = filename
        self.content_type = content_type
        self.data = data

    def __repr__(self):
        return "FormPart({!r}, {!r}, {!r}, {} bytes)".format(
            self.name, self.filename, self.content_type, len(self.data)
        )


class RecordedRequest:
    def __init__(self, method, target, headers, body):
        url = urlsplit(target)
        self.method = method
        # The path after the API prefix; url_path is the whole path, for
        # requests elsewhere, such as to a signed transfer URL.
        self.url_path = url.path
        self.path = url.path[len(API_PREFIX) :]
        self.query = dict(parse_qsl(url.query, keep_blank_values=True))
        # As sent, so a test can see every repetition of a name.
        self.query_string = url.query
        self.headers = headers
        self.body = body

    @property
    def json(self):
        """A JSON body, parsed; None for any other body. A body the client
        abandoned part way is not parsed until a test asks for it."""
        is_json = self.headers.get("Content-Type", "").startswith(
            "application/json"
        )
        return json.loads(self.body) if self.body and is_json else None

    @property
    def complete(self):
        """Whether the whole body its Content-Length announced arrived."""
        return len(self.body) == int(self.headers.get("Content-Length") or 0)

    @property
    def form(self):
        """The parts of a multipart/form-data body, parsed by the standard
        library's MIME parser."""
        content_type = self.headers["Content-Type"]
        if not content_type.startswith("multipart/form-data;"):
            raise AssertionError(f"Not a multipart request: {content_type}")
        message = email.parser.BytesParser(
            policy=email.policy.HTTP
        ).parsebytes(
            b"Content-Type: " + content_type.encode() + b"\r\n\r\n" + self.body
        )
        if message.defects:
            raise AssertionError(
                f"Malformed multipart body: {message.defects}"
            )
        return [
            FormPart(
                part.get_param("name", header="Content-Disposition"),
                part.get_filename(),
                part.get("Content-Type"),
                part.get_payload(decode=True),
            )
            for part in message.iter_parts()
        ]

    def form_values(self):
        """The text fields of a multipart body, as (name, text) pairs."""
        return [
            (part.name, part.data.decode())
            for part in self.form
            if part.filename is None
        ]

    def form_file(self, name):
        [part] = [part for part in self.form if part.name == name]
        return part


class LoopbackApi:
    """A local Files.com API stand-in that plays back scripted responses and
    records every request, so tests run the SDK's real HTTP stack."""

    def __init__(self, tls=None):
        self.requests = []
        self.responses = []
        self._arrived = threading.Condition()
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), self._handler())
        self.port = self.server.server_port
        self.url = "http://127.0.0.1:{}".format(self.port)
        if tls is not None:
            # tls is a tests.network_fixtures.TestAuthority.
            self.server.socket = tls.server_context().wrap_socket(
                self.server.socket, server_side=True
            )
            self.url = "https://localhost:{}".format(self.port)

    def reply(self, status=200, body=b"", headers=None, when_received=None):
        """Answer the next request. when_received, if given, runs after the
        request has arrived and before the answer is sent."""
        self.responses.append(
            (status, dict(headers or {}), body, when_received)
        )

    def reply_json(self, value, status=200, headers=None, when_received=None):
        headers = {"Content-Type": "application/json", **(headers or {})}
        self.reply(status, json.dumps(value).encode(), headers, when_received)

    def wait_for_requests(self, count, timeout=5):
        """The recorded requests, once count have arrived. The server records
        a request the client abandoned only when it sees the connection
        close, which can be after the client has raised."""
        with self._arrived:
            self._arrived.wait_for(
                lambda: len(self.requests) >= count, timeout
            )
        return self.requests

    def disconnect(self, after_body_bytes):
        """Read only this much of the next request's body, then close the
        connection without answering."""
        self.responses.append(after_body_bytes)

    def _handler(self):
        api = self

        class Handler(BaseHTTPRequestHandler):
            def serve(self):
                length = int(self.headers.get("Content-Length") or 0)
                script = api.responses.pop(0) if api.responses else None
                if isinstance(script, int):
                    length = min(length, script)
                request = RecordedRequest(
                    self.command,
                    self.path,
                    self.headers,
                    self.rfile.read(length),
                )
                with api._arrived:
                    api.requests.append(request)
                    api._arrived.notify_all()
                if isinstance(script, int) or not request.complete:
                    self.close_connection = True
                    return
                status, headers, body, when_received = script or (
                    500,
                    {},
                    b"no scripted response",
                    None,
                )
                if when_received:
                    when_received()
                try:
                    self.send_response(status)
                    for name, value in headers.items():
                        self.send_header(name, value)
                    self.send_header("Content-Length", str(len(body)))
                    self.end_headers()
                    self.wfile.write(body)
                except ConnectionError:
                    self.close_connection = True  # The client gave up.

            do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = serve

            def log_message(self, *args):
                pass

        return Handler


def start_loopback_api(test_case, tls=None):
    """A new LoopbackApi that serves until the test ends."""
    api = LoopbackApi(tls)
    thread = threading.Thread(
        target=api.server.serve_forever, kwargs={"poll_interval": 0.005}
    )
    thread.start()
    test_case.addCleanup(thread.join)
    test_case.addCleanup(api.server.server_close)
    test_case.addCleanup(api.server.shutdown)
    return api


def serve_loopback_api(test_case, max_network_retries=0):
    """Point the module-level functions at a new LoopbackApi for the
    duration of a test.

    By default each call makes one HTTP attempt, so request counts reflect
    what the SDK decided to send rather than the retry policy. Retries,
    when a test allows them, do not wait.
    """
    api = start_loopback_api(test_case)
    for name, value in {
        "base_url": api.url,
        "the_api_key": "globalkey",
        "session_id": None,
        "workspace_id": None,
        "max_network_retries": max_network_retries,
        "initial_network_retry_delay": 0,
        "max_network_retry_delay": 0,
        "console_log_level": "none",
    }.items():
        patcher = patch.object(files_sdk, name, value)
        patcher.start()
        test_case.addCleanup(patcher.stop)
    return api

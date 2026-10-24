import io
import json
import random
import socket
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

import files_sdk
import requests
from files_sdk.error import (
    APIConnectionError,
    ClientClosedError,
    DeadlineExceededError,
    InvalidParameterError,
    NotFoundError,
    OperationCancelledError,
)
from tests.loopback_api import serve_loopback_api, start_loopback_api
from tests.network_fixtures import WAIT, ScriptedServer, TestAuthority

# Requests blocked on the network settle within this many seconds of being
# stopped. The owned transport measured well under 10 ms; this leaves room
# for loaded CI machines.
PROMPT = 2


def api_script(routes):
    """A keep-alive server script. routes maps a path, such as
    "/api/rest/v1/users/1", to (status, JSON body) or to a function that
    takes the peer and answers, or never does."""

    def script(peer):
        while True:
            first, _headers, _body = peer.read_request()
            path = first.split()[1].split("?")[0]
            route = routes.get(
                path, (404, {"type": "not-found", "error": "Not Found"})
            )
            if callable(route):
                route(
                    peer
                )  # A route that blocks returns once the client has gone.
                continue
            status, body = route
            peer.respond(
                status,
                json.dumps(body).encode(),
                {"Content-Type": "application/json"},
            )

    return script


def block(peer):
    peer.record.received.set()
    peer.wait_for_close()


def trickle(peer):
    peer.send(b"HTTP/1.1 200 OK\r\nContent-Length: 1000000\r\n\r\n")
    peer.record.received.set()
    try:
        while True:
            peer.send(b"x")
            time.sleep(0.02)
    except OSError:
        pass


class Worker:
    """Runs call in a thread and records what it returned or raised."""

    def __init__(self, call):
        self.result = self.error = self.finished_at = None
        self.thread = threading.Thread(target=self._run, args=(call,))
        self.thread.start()

    def _run(self, call):
        try:
            self.result = call()
        except BaseException as error:
            self.error = error
        self.finished_at = time.monotonic()

    def join(self):
        self.thread.join(WAIT)
        return self


def wait_until(condition):
    deadline = time.monotonic() + WAIT
    while not condition() and time.monotonic() < deadline:
        time.sleep(0.005)
    return condition()


class TestRequestsOverTls(unittest.TestCase):
    """Requests to a TLS server: stopped as promptly as plain ones, and
    otherwise sent whole."""

    def setUp(self):
        self.authority = TestAuthority.create(self)

    def test_large_requests_arrive_whole_and_share_one_connection(self):
        bodies = []

        def save(peer):
            bodies.append(peer.record.body)
            peer.respond(
                200,
                json.dumps({"id": 1}).encode(),
                {"Content-Type": "application/json"},
            )

        server = ScriptedServer(
            self,
            api_script({"/api/rest/v1/users/1": save}),
            tls=self.authority,
        )
        client = files_sdk.Client(
            api_key="key", base_url=server.url(""), verify=self.authority.ca
        )
        self.addCleanup(client.close)
        # More than socket buffers usually take at once, so each is sent in pieces.
        names = [
            random.Random(seed).randbytes(2 * 1024 * 1024).hex()
            for seed in (1, 2)
        ]

        user = client.user.find(1)
        for name in names:
            user.update({"name": name})

        lookup, *updates = bodies
        self.assertEqual(b"", lookup)
        self.assertEqual(names, [json.loads(body)["name"] for body in updates])
        self.assertEqual(1, len(server.connections))

    def test_a_cancelled_upload_stops_sending_and_never_completes(self):
        release = threading.Event()

        def stall(peer):
            peer.record.received.set()
            release.wait(WAIT * 3)
            peer.wait_for_close()

        storage = ScriptedServer(self, stall, tls=self.authority)
        api = start_loopback_api(self)
        partsize = 32 * 1024 * 1024
        api.reply_json(
            [
                {
                    "ref": "ref1",
                    "part_number": 1,
                    "partsize": partsize,
                    "http_method": "PUT",
                    "upload_uri": storage.url("/part1"),
                }
            ]
        )
        client = files_sdk.Client(
            api_key="key", base_url=api.url, verify=self.authority.ca
        )
        self.addCleanup(client.close)
        token = files_sdk.CancellationToken()
        with tempfile.TemporaryDirectory() as directory:
            local = Path(directory) / "big.bin"
            local.write_bytes(b"u" * partsize)
            worker = Worker(
                lambda: client.file.upload_file(
                    local, "big.bin", {"cancel_token": token}
                )
            )
            # Storage has finished the TLS handshake and reads nothing more.
            self.assertTrue(
                wait_until(
                    lambda: storage.connections
                    and storage.connections[0].received.is_set()
                )
            )
            time.sleep(0.2)  # Let the part fill the socket buffers.

            cancelled_at = time.monotonic()
            token.cancel()
            worker.join()
            release.set()

        self.assertIsInstance(worker.error, OperationCancelledError)
        self.assertLess(worker.finished_at - cancelled_at, PROMPT)
        self.assertTrue(storage.connections[0].closed.wait(WAIT))
        self.assertEqual(
            ["/file_actions/begin_upload/big.bin"],
            [request.path for request in api.requests],
        )

    def test_a_cancelled_request_stops_waiting_for_its_response(self):
        server = ScriptedServer(
            self,
            api_script(
                {
                    "/api/rest/v1/users/1": (200, {"id": 1}),
                    "/api/rest/v1/users/2": block,
                }
            ),
            tls=self.authority,
        )
        client = files_sdk.Client(
            api_key="key", base_url=server.url(""), verify=self.authority.ca
        )
        self.addCleanup(client.close)
        client.user.find(1)
        token = files_sdk.CancellationToken()
        worker = Worker(
            lambda: client.user.find(2, {}, {"cancel_token": token})
        )
        # The server has read the whole request and holds back its answer.
        self.assertTrue(server.connections[0].received.wait(WAIT))

        cancelled_at = time.monotonic()
        token.cancel()
        worker.join()

        self.assertIsInstance(worker.error, OperationCancelledError)
        self.assertTrue(worker.error.remote_outcome_unknown)
        self.assertLess(worker.finished_at - cancelled_at, PROMPT)
        self.assertTrue(server.connections[0].closed.wait(WAIT))
        client.user.find(1)
        self.assertEqual(2, len(server.connections))


class TestConnectionsAndClose(unittest.TestCase):
    def test_requests_share_one_connection_until_close(self):
        answers = iter(
            [
                (503, {"type": "processing-failure/unknown", "error": "Busy"}),
                (200, {"id": 3}),
            ]
        )

        def busy_then_ok(peer):
            status, body = next(answers)
            peer.respond(
                status,
                json.dumps(body).encode(),
                {"Content-Type": "application/json"},
            )

        def malformed(peer):
            peer.respond(
                200, b"not json", {"Content-Type": "application/json"}
            )

        server = ScriptedServer(
            self,
            api_script(
                {
                    "/api/rest/v1/users/1": (200, {"id": 1, "name": "Pat"}),
                    "/api/rest/v1/users": (200, [{"id": 1}, {"id": 2}]),
                    "/api/rest/v1/users/2": (
                        404,
                        {"type": "not-found", "error": "Not Found"},
                    ),
                    "/api/rest/v1/users/3": busy_then_ok,
                    "/api/rest/v1/users/4": malformed,
                }
            ),
        )
        client = files_sdk.Client(
            api_key="key",
            base_url=server.url(""),
            initial_network_retry_delay=0,
        )
        user = client.user.find(1)
        page = client.user.list()
        with self.assertRaises(NotFoundError):
            client.user.find(2)
        self.assertEqual(3, client.user.find(3).id)
        with self.assertRaises(APIConnectionError):
            client.user.find(4)
        user.update({"name": "Robin"})

        client.close()
        client.close()

        self.assertEqual(1, len(server.connections))
        self.assertTrue(server.connections[0].closed.wait(WAIT))
        with self.assertRaises(ClientClosedError):
            user.save()
        with self.assertRaises(ClientClosedError):
            client.user.find(1)
        self.assertEqual([1, 2], [item.id for item in page])
        self.assertEqual("Pat", user.name)
        self.assertEqual(1, len(server.connections))

    def test_close_ends_idle_connections_while_an_earlier_error_is_kept(self):
        def hang_up(peer):
            raise OSError("closed without answering")

        server = ScriptedServer(
            self,
            api_script(
                {
                    "/api/rest/v1/users/1": (200, {"id": 1}),
                    "/api/rest/v1/users/2": hang_up,
                }
            ),
        )
        # Downloads from ten other origins, as signed URLs can be, push the
        # API's pool out of urllib3's cache of recent pools while the kept
        # error still refers to it.
        storage = [
            ScriptedServer(self, api_script({"/file": (200, {})}))
            for _ in range(10)
        ]
        client = files_sdk.Client(
            api_key="key", base_url=server.url(""), max_network_retries=0
        )
        with self.assertRaises(APIConnectionError) as failed:
            client.user.find(2)
        kept = failed.exception  # As an application might, to report it later.
        client.user.find(1)
        for origin in storage:
            remote = client.file.new(
                {"path": "file", "download_uri": origin.url("/file")}
            )
            remote.download_content(io.BytesIO())

        client.close()

        self.assertEqual(2, len(server.connections))
        self.assertTrue(server.connections[1].closed.wait(WAIT))
        self.assertTrue(
            all(origin.connections[0].closed.wait(WAIT) for origin in storage)
        )
        self.assertIsNotNone(kept.__cause__ or kept.__context__)

    def test_a_retained_page_reads_after_close_but_cannot_advance(self):
        api = start_loopback_api(self)
        api.reply_json([{"id": 1}], headers={"X-Files-Cursor": "next"})
        client = files_sdk.Client(api_key="key", base_url=api.url)
        page = client.user.list()

        client.close()

        self.assertEqual([1], [item.id for item in page])
        with self.assertRaises(ClientClosedError):
            page.load_next_page()
        self.assertEqual(1, len(api.requests))

    def test_a_borrowed_session_carries_every_request_and_stays_open(self):
        api = start_loopback_api(self)
        seen = []
        session = requests.Session()
        self.addCleanup(session.close)
        session.hooks["response"].append(
            lambda response, **_: seen.append(response.request.url)
        )
        # Credentials the session adds to its own requests, which a signed
        # transfer URL must not receive.
        session.auth = ("user", "private-password")
        session.headers["X-Company-Token"] = "private-token"
        session.cookies.set("sessioncookie", "private-cookie")
        api.reply_json(
            {
                "path": "doc.txt",
                "download_uri": api.url
                + "/storage/doc.txt?X-Amz-Signature=secret",
            }
        )
        api.reply(200, b"content")
        client = files_sdk.Client(
            api_key="key", base_url=api.url, http_session=session
        )

        with tempfile.TemporaryDirectory() as directory:
            local = Path(directory) / "doc.txt"
            client.file.download_file("doc.txt", local)
            self.assertEqual(b"content", local.read_bytes())
        client.close()

        # The download asks for a download identity; without one, the file
        # is read in one response.
        self.assertEqual(
            [
                api.url
                + "/api/rest/v1/files/doc.txt?path=doc.txt&with_download_identity=True",
                api.url + "/storage/doc.txt?X-Amz-Signature=secret",
            ],
            seen,
        )
        lookup, transfer = api.requests
        self.assertEqual("private-token", lookup.headers["X-Company-Token"])
        self.assertIn("Authorization", lookup.headers)
        for header in (
            "Authorization",
            "X-Company-Token",
            "Cookie",
            "X-FilesAPI-Key",
        ):
            self.assertNotIn(header, transfer.headers)
        api.reply(200, b"still open")
        self.assertEqual(
            b"still open", session.get(api.url + "/after").content
        )
        self.assertEqual(
            "private-cookie",
            api.requests[-1].headers["Cookie"].split("=", 1)[1],
        )

    def test_uploads_refuse_a_borrowed_session_that_retries_on_its_own(self):
        api = start_loopback_api(self)
        session = requests.Session()
        self.addCleanup(session.close)
        session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
        client = files_sdk.Client(
            api_key="key", base_url=api.url, http_session=session
        )
        self.addCleanup(client.close)

        with tempfile.TemporaryDirectory() as directory:
            local = Path(directory) / "file.txt"
            local.write_bytes(b"hello")
            with self.assertRaises(InvalidParameterError):
                client.file.upload_file(local, "file.txt")
        with self.assertRaises(InvalidParameterError):
            with client.file.open("notes.txt", "w") as remote:
                remote.write("hello")

        self.assertEqual([], api.requests)

    def test_closing_one_client_leaves_another_and_its_token_alone(self):
        api = start_loopback_api(self)
        first = files_sdk.Client(api_key="first", base_url=api.url)
        second = files_sdk.Client(api_key="second", base_url=api.url)
        self.addCleanup(second.close)
        token = files_sdk.CancellationToken()
        api.reply_json({"id": 1})

        first.close()
        second.user.find(1, {}, {"cancel_token": token})

        self.assertFalse(token.cancelled)
        self.assertEqual("second", api.requests[0].headers["X-FilesAPI-Key"])

    def test_sessions_the_sdk_creates_keep_no_server_cookies(self):
        # A cookie set while one principal was in use must not ride along
        # with another's request. A caller's own session keeps Requests'
        # usual cookie handling.
        for label in ("owned", "borrowed"):
            with self.subTest(session=label):
                api = start_loopback_api(self)
                session = None if label == "owned" else requests.Session()
                if session is not None:
                    self.addCleanup(session.close)
                client = files_sdk.Client(
                    api_key="keyA", base_url=api.url, http_session=session
                )
                self.addCleanup(client.close)
                api.reply_json(
                    {"id": 1}, headers={"Set-Cookie": "affinity=keyA; Path=/"}
                )
                api.reply_json({"id": 2})

                client.user.find(1)
                client.user.find(2, {}, {"api_key": "keyB"})

                cookie = api.requests[1].headers.get("Cookie")
                self.assertEqual(
                    None if label == "owned" else "affinity=keyA", cookie
                )

    def test_the_deadline_thread_ends_once_no_deadline_is_pending(self):
        api = start_loopback_api(self)
        client = files_sdk.Client(
            api_key="key", base_url=api.url, request_timeout=86400
        )
        api.reply_json({"id": 1})

        client.user.find(1)
        client.close()

        self.assertTrue(
            wait_until(
                lambda: not any(
                    t.name == "files_sdk deadlines"
                    for t in threading.enumerate()
                )
            )
        )


class TestModuleClose(unittest.TestCase):
    def test_files_sdk_close_ends_the_module_connections_and_their_objects(
        self,
    ):
        api = serve_loopback_api(self)
        api.reply_json({"id": 1})
        user = files_sdk.user.find(1)

        files_sdk.close()
        files_sdk.close()

        with self.assertRaises(ClientClosedError):
            user.save()
        api.reply_json({"id": 2})
        self.assertEqual(2, files_sdk.user.find(2).id)
        self.assertEqual(2, len(api.requests))


class TestCancellation(unittest.TestCase):
    def blocked_client(self, route=block, **settings):
        server = ScriptedServer(
            self,
            api_script(
                {
                    "/api/rest/v1/users/1": (200, {"id": 1}),
                    "/api/rest/v1/users/2": route,
                }
            ),
        )
        client = files_sdk.Client(
            api_key="key", base_url=server.url(""), **settings
        )
        self.addCleanup(client.close)
        return server, client

    def test_cancelling_stops_a_blocked_request_at_once_and_discards_its_connection(
        self,
    ):
        server, client = self.blocked_client()
        client.user.find(1)
        token = files_sdk.CancellationToken()
        worker = Worker(
            lambda: client.user.find(2, {}, {"cancel_token": token})
        )
        self.assertTrue(server.connections[0].received.wait(WAIT))

        cancelled_at = time.monotonic()
        token.cancel()
        worker.join()

        self.assertIsInstance(worker.error, OperationCancelledError)
        self.assertTrue(worker.error.remote_outcome_unknown)
        self.assertLess(worker.finished_at - cancelled_at, PROMPT)
        self.assertTrue(server.connections[0].closed.wait(WAIT))
        client.user.find(1)
        self.assertEqual(2, len(server.connections))

    def test_a_deadline_stops_a_response_that_keeps_trickling(self):
        server, client = self.blocked_client(
            route=trickle, request_timeout=0.5
        )
        started = time.monotonic()

        with self.assertRaises(DeadlineExceededError):
            client.user.find(2)

        self.assertLess(time.monotonic() - started, 0.5 + PROMPT)

    def test_closing_the_client_stops_its_blocked_request(self):
        server, client = self.blocked_client()
        worker = Worker(lambda: client.user.find(2))
        self.assertTrue(
            wait_until(
                lambda: server.connections
                and server.connections[0].received.is_set()
            )
        )

        closed_at = time.monotonic()
        client.close()
        close_returned = time.monotonic()
        worker.join()

        self.assertIsInstance(worker.error, ClientClosedError)
        self.assertLess(close_returned - closed_at, PROMPT)
        self.assertLessEqual(worker.finished_at, close_returned)
        with self.assertRaises(ClientClosedError):
            client.user.find(1)
        self.assertEqual(1, len(server.connections))

    def test_closing_from_inside_a_download_fails_instead_of_deadlocking(self):
        api = start_loopback_api(self)
        client = files_sdk.Client(api_key="key", base_url=api.url)
        self.addCleanup(client.close)
        api.reply_json(
            {"path": "doc.txt", "download_uri": api.url + "/storage/doc.txt"}
        )
        api.reply(200, b"content")

        class Destination:
            def write(self, _data):
                client.close()

        with self.assertRaises(RuntimeError):
            client.file.find("doc.txt").download_content(Destination())
        self.assertFalse(client.closed)

    def test_a_cancelled_upload_stops_sending_and_never_completes(self):
        release = threading.Event()

        def stall(peer):
            peer.record.received.set()
            release.wait(WAIT * 3)
            peer.wait_for_close()

        storage = ScriptedServer(self, stall)
        api = start_loopback_api(self)
        partsize = 32 * 1024 * 1024
        api.reply_json(
            [
                {
                    "ref": "ref1",
                    "part_number": 1,
                    "partsize": partsize,
                    "http_method": "PUT",
                    "upload_uri": storage.url("/part1"),
                }
            ]
        )
        client = files_sdk.Client(api_key="key", base_url=api.url)
        self.addCleanup(client.close)
        token = files_sdk.CancellationToken()
        with tempfile.TemporaryDirectory() as directory:
            local = Path(directory) / "big.bin"
            local.write_bytes(b"u" * partsize)
            worker = Worker(
                lambda: client.file.upload_file(
                    local, "big.bin", {"cancel_token": token}
                )
            )
            self.assertTrue(
                wait_until(
                    lambda: storage.connections
                    and storage.connections[0].received.is_set()
                )
            )
            time.sleep(0.2)  # Let the part fill the socket buffers.

            cancelled_at = time.monotonic()
            token.cancel()
            worker.join()
            release.set()

        self.assertIsInstance(worker.error, OperationCancelledError)
        self.assertLess(worker.finished_at - cancelled_at, PROMPT)
        self.assertTrue(storage.connections[0].closed.wait(WAIT))
        self.assertEqual(
            ["/file_actions/begin_upload/big.bin"],
            [request.path for request in api.requests],
        )

    def test_a_request_through_a_callers_session_does_not_succeed_after_cancellation(
        self,
    ):
        # The SDK cannot interrupt a session it did not create, but once the
        # request returns, a cancelled operation raises. The response that
        # arrived afterwards stays on the error, unused.
        api = start_loopback_api(self)
        session = requests.Session()
        self.addCleanup(session.close)
        client = files_sdk.Client(
            api_key="key", base_url=api.url, http_session=session
        )
        self.addCleanup(client.close)
        token = files_sdk.CancellationToken()
        api.reply_json({"id": 1}, when_received=token.cancel)
        api.reply_json({"id": 2})

        with self.assertRaises(OperationCancelledError) as caught:
            client.user.find(1, {}, {"cancel_token": token})
        # Cancelling after a response arrived changes nothing.
        other = files_sdk.CancellationToken()
        user = client.user.find(2, {}, {"cancel_token": other})
        other.cancel()

        self.assertTrue(caught.exception.remote_outcome_unknown)
        self.assertEqual(200, caught.exception.response.status_code)
        self.assertEqual(2, user.id)

    def test_file_helpers_keep_the_callers_token_and_deadline(self):
        cancelled = files_sdk.CancellationToken()
        cancelled.cancel()
        api = start_loopback_api(self)
        client = files_sdk.Client(api_key="key", base_url=api.url)
        self.addCleanup(client.close)
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "report.csv"
            destination.write_bytes(b"kept")
            for options in (
                {"cancel_token": cancelled},
                {"deadline": time.monotonic() - 1},
            ):
                with self.subTest(options=options):
                    with self.assertRaises(
                        (OperationCancelledError, DeadlineExceededError)
                    ):
                        client.file.download_file(
                            "report.csv", destination, options
                        )
                    with self.assertRaises(
                        (OperationCancelledError, DeadlineExceededError)
                    ):
                        with client.file.open(
                            "notes.txt", "wb", options
                        ) as remote:
                            remote.write(b"hello")
            # A file stopped after it was opened downloads nothing either.
            token = files_sdk.CancellationToken()
            with client.file.open(
                "report.csv", "rb", {"cancel_token": token}
            ) as remote:
                token.cancel()
                with self.assertRaises(OperationCancelledError):
                    remote.download_file(destination)
                with self.assertRaises(OperationCancelledError):
                    remote.download_uri_with_load()
            with client.file.open(
                "report.csv", "rb", {"request_timeout": 0.05}
            ) as remote:
                time.sleep(0.1)
                with self.assertRaises(DeadlineExceededError):
                    remote.download_file(destination)
            self.assertEqual(b"kept", destination.read_bytes())
        self.assertEqual([], api.requests)

    def test_an_opened_files_operation_ends_when_it_closes(self):
        api = start_loopback_api(self)
        api.reply_json(
            {"path": "report.csv", "download_uri": api.url + "/storage/report"}
        )
        api.reply(200, b"first")
        api.reply(200, b"second")
        client = files_sdk.Client(api_key="key", base_url=api.url)
        self.addCleanup(client.close)
        token = files_sdk.CancellationToken()

        remote = client.file.open("report.csv", "rb", {"cancel_token": token})
        self.assertEqual(b"first", remote.read())
        remote.close()
        token.cancel()
        later = io.BytesIO()
        remote.download_content(later)

        self.assertEqual(b"second", later.getvalue())
        self.assertEqual(3, len(api.requests))

    def test_a_deadline_given_to_open_covers_the_upload_close_finishes(self):
        api = start_loopback_api(self)
        api.reply_json(
            [
                {
                    "ref": "ref1",
                    "part_number": 1,
                    "partsize": 1024,
                    "http_method": "PUT",
                    "upload_uri": api.url + "/storage/part1",
                }
            ]
        )
        client = files_sdk.Client(api_key="key", base_url=api.url)
        self.addCleanup(client.close)

        with self.assertRaises(DeadlineExceededError):
            with client.file.open(
                "notes.txt", "wb", {"request_timeout": 0.2}
            ) as remote:
                remote.write(
                    b"hello"
                )  # Asks for the first part, to learn its size.
                time.sleep(0.4)

        # Nothing was sent to storage and the upload was not completed.
        self.assertEqual(
            ["/file_actions/begin_upload/notes.txt"],
            [request.path for request in api.requests],
        )

    def test_cancelling_other_requests_never_stops_an_uncancelled_one(self):
        server = ScriptedServer(
            self, api_script({"/api/rest/v1/users/1": (200, {"id": 1})})
        )
        client = files_sdk.Client(api_key="key", base_url=server.url(""))
        self.addCleanup(client.close)
        stop = threading.Event()
        failures = []

        def innocent():
            while not stop.is_set():
                try:
                    client.user.find(1)
                except Exception as error:
                    failures.append(error)

        runner = threading.Thread(target=innocent)
        runner.start()
        rng = random.Random(25)
        for _ in range(60):
            token = files_sdk.CancellationToken()
            worker = Worker(
                lambda: client.user.find(1, {}, {"cancel_token": token})
            )
            time.sleep(rng.uniform(0, 0.003))
            token.cancel()
            worker.join()
            self.assertTrue(
                worker.error is None
                or isinstance(worker.error, OperationCancelledError),
                worker.error,
            )
        stop.set()
        runner.join(WAIT)

        self.assertEqual([], failures)


class TestScriptedServer(unittest.TestCase):
    """The loopback server these tests stop as they clean up, when the
    connections of requests they stopped can still be arriving."""

    def test_a_connection_accepted_as_the_server_stops_is_closed_without_being_served(
        self,
    ):
        accepted, resume = threading.Event(), threading.Event()

        class Listener(socket.socket):
            def accept(self):
                # The server has accepted a connection, and has it only once
                # the test has stopped the server.
                connection = super().accept()
                accepted.set()
                resume.wait(WAIT)
                return connection

        listener = Listener()
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        served = []
        with mock.patch.object(socket, "create_server", return_value=listener):
            server = ScriptedServer(self, served.append)
        client = socket.create_connection(("127.0.0.1", server.port))
        self.addCleanup(client.close)
        self.assertTrue(accepted.wait(WAIT))

        server.stop()
        resume.set()

        client.settimeout(WAIT)
        self.assertEqual(b"", client.recv(1))
        self.assertEqual(([], []), (served, server.connections))


if __name__ == "__main__":
    unittest.main()

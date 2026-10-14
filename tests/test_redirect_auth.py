import os
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import files_sdk
import requests
from files_sdk.api import Operation
from files_sdk.api_client import ApiClient
from files_sdk.error import APIConnectionError, InvalidRequestError
from tests.loopback_api import start_loopback_api
from tests.network_fixtures import TestAuthority


class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/rest/v1/cross-origin":
            self.send_response(302)
            self.send_header(
                "Location", self.server.cross_origin_url + "/download"
            )
            self.end_headers()
            return
        if self.path == "/api/rest/v1/same-origin":
            self.send_response(302)
            self.send_header("Location", "/api/rest/v1/final")
            self.end_headers()
            return
        if self.path == "/api/rest/v1/round-trip":
            self.send_response(307)
            self.send_header(
                "Location", self.server.cross_origin_url + "/return"
            )
            self.end_headers()
            return
        if self.path.startswith("/api/rest/v1/folders/redirect-out"):
            self.server.received_headers.append(self.headers)
            self.send_response(302)
            self.send_header(
                "Location", self.server.cross_origin_url + "/listing"
            )
            self.end_headers()
            return
        if self.path == "/listing":
            self.server.received_headers.append(self.headers)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", "2")
            self.end_headers()
            self.wfile.write(b"[]")
            return
        if self.path == "/return":
            self.send_response(302)
            self.send_header(
                "Location",
                self.server.cross_origin_url + "/api/rest/v1/landing",
            )
            self.end_headers()
            return

        self.server.received_headers.append(self.headers)
        self.send_response(204)
        self.end_headers()

    def do_PUT(self):
        self._with_body()

    def do_POST(self):
        self._with_body()

    def _with_body(self):
        body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
        self.server.received_bodies.append((self.path, body))
        if self.path in (
            "/part-cross-origin",
            "/api/rest/v1/users-cross-origin",
        ):
            self.send_response(307)
            self.send_header(
                "Location", self.server.cross_origin_url + "/landing"
            )
            self.end_headers()
            return
        if self.path == "/part-same-origin":
            self.send_response(307)
            self.send_header("Location", "/landing")
            self.end_headers()
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", "2")
        self.end_headers()
        self.wfile.write(b"{}")

    def log_message(self, *args):
        pass


class TestRedirectAuth(unittest.TestCase):
    def setUp(self):
        self.api_server = ThreadingHTTPServer(
            ("127.0.0.1", 0), RedirectHandler
        )
        self.storage_server = ThreadingHTTPServer(
            ("127.0.0.1", 0), RedirectHandler
        )
        self.api_server.received_headers = []
        self.storage_server.received_headers = []
        self.api_server.received_bodies = []
        self.storage_server.received_bodies = []
        self.api_url = "http://127.0.0.1:{}".format(
            self.api_server.server_port
        )
        self.storage_url = "http://127.0.0.1:{}".format(
            self.storage_server.server_port
        )
        self.api_server.cross_origin_url = self.storage_url
        self.storage_server.cross_origin_url = self.api_url
        self.threads = [
            threading.Thread(
                target=self.api_server.serve_forever,
                kwargs={"poll_interval": 0.005},
            ),
            threading.Thread(
                target=self.storage_server.serve_forever,
                kwargs={"poll_interval": 0.005},
            ),
        ]
        for thread in self.threads:
            thread.start()

        self.original_base_url = files_sdk.base_url
        files_sdk.base_url = self.api_url

    def tearDown(self):
        files_sdk.base_url = self.original_base_url
        files_sdk.set_workspace_id(None)
        for server in (self.api_server, self.storage_server):
            server.shutdown()
            server.server_close()
        for thread in self.threads:
            thread.join()

    def test_cross_origin_redirect_strips_files_auth_headers(self):
        client = ApiClient()
        client.send_request(
            "GET",
            "/cross-origin",
            session_id="testsession",
            workspace_id=123,
            params={},
        )

        redirected_headers = self.storage_server.received_headers[0]
        self.assertNotIn("X-FilesAPI-Key", redirected_headers)
        self.assertNotIn("X-FilesAPI-Auth", redirected_headers)
        self.assertNotIn("X-Files-Workspace-Id", redirected_headers)

    def test_a_chain_that_leaves_and_returns_to_the_origin_stays_stripped(
        self,
    ):
        # 127.0.0.1 on another port is another origin.
        ApiClient().send_request(
            "GET",
            "/round-trip",
            api_key="testkey",
            workspace_id=123,
            params={},
        )

        [landing] = self.api_server.received_headers
        for header in (
            "X-FilesAPI-Key",
            "X-FilesAPI-Auth",
            "X-Files-Workspace-Id",
        ):
            self.assertNotIn(header, landing)

    def test_a_borrowed_session_s_credentials_stay_on_the_api_origin(self):
        session = requests.Session()
        self.addCleanup(session.close)
        session.auth = ("user", "private-password")
        session.headers["X-Company-Token"] = "private-token"
        client = files_sdk.Client(
            api_key="clientkey", base_url=self.api_url, http_session=session
        )
        self.addCleanup(client.close)

        self.assertEqual([], list(client.folder.list_for("redirect-out")))

        [api] = self.api_server.received_headers
        [storage] = self.storage_server.received_headers
        self.assertEqual(
            ("clientkey", "private-token"),
            (api["X-FilesAPI-Key"], api["X-Company-Token"]),
        )
        self.assertIn("Authorization", api)
        for header in (
            "Authorization",
            "X-Company-Token",
            "X-FilesAPI-Key",
            "X-Files-Workspace-Id",
        ):
            self.assertNotIn(header, storage)

    def test_session_authentication_cannot_send_credentials_to_another_origin(
        self,
    ):
        # Requests lets a session's authentication change the prepared
        # request; the SDK refuses to send its credentials elsewhere, and
        # authentication that stays at the API origin keeps working.
        storage_url = self.storage_url

        class Retarget(requests.auth.AuthBase):
            def __call__(self, request):
                request.url = storage_url + "/elsewhere"
                return request

        session = requests.Session()
        self.addCleanup(session.close)
        session.auth = Retarget()
        client = files_sdk.Client(
            api_key="clientkey",
            workspace_id=5,
            base_url=self.api_url,
            http_session=session,
        )
        self.addCleanup(client.close)

        with self.assertRaises(InvalidRequestError):
            client.folder.list_for("redirect-out")

        self.assertEqual([], self.api_server.received_headers)
        self.assertEqual([], self.storage_server.received_headers)

    def test_credentials_in_a_netrc_file_are_never_sent(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".netrc", delete=False
        ) as netrc:
            netrc.write(
                "machine 127.0.0.1 login netrcuser password netrcpassword\n"
            )
        self.addCleanup(os.remove, netrc.name)
        with patch.dict(os.environ, {"NETRC": netrc.name}):
            # Requests on its own sends them, so the file is in effect.
            requests.get(
                self.api_url + "/api/rest/v1/final", timeout=5
            ).close()
            ApiClient().send_request(
                "GET", "/same-origin", api_key="testkey", params={}
            )
            ApiClient().send_request(
                "GET", "/cross-origin", api_key="testkey", params={}
            )

        control, same_origin = self.api_server.received_headers
        [cross_origin] = self.storage_server.received_headers
        self.assertIn("Authorization", control)
        self.assertNotIn("Authorization", same_origin)
        self.assertNotIn("Authorization", cross_origin)

    def test_a_redirect_that_would_carry_a_body_to_another_origin_is_not_followed(
        self,
    ):
        # A 307 keeps the request's body. Within the origin it is followed;
        # to another origin the body stays behind, and nothing is sent there.
        # The request's own origin had it once and answered, so what it
        # asked for may have happened there.
        client = ApiClient()
        response = client.send_remote_request(
            "PUT", self.storage_url + "/part-same-origin", body=b"part"
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            [("/part-same-origin", b"part"), ("/landing", b"part")],
            self.storage_server.received_bodies,
        )

        for name, send in (
            (
                "an upload part",
                lambda: client.send_remote_request(
                    "PUT",
                    self.storage_url + "/part-cross-origin",
                    body=b"part",
                ),
            ),
            (
                "an API request",
                lambda: client.send_request(
                    "POST",
                    "/users-cross-origin",
                    api_key="testkey",
                    params={"name": "x"},
                ),
            ),
        ):
            with self.subTest(name):
                with self.assertRaises(APIConnectionError) as caught:
                    send()
                self.assertIn("not followed", str(caught.exception))
                self.assertEqual(
                    ("response", True),
                    (
                        caught.exception.phase,
                        caught.exception.remote_outcome_unknown,
                    ),
                )
                if name == "an API request":
                    self.assertIn(
                        "Check whether it took effect before repeating it.",
                        str(caught.exception),
                    )
        self.assertEqual(
            [
                ("/part-same-origin", b"part"),
                ("/landing", b"part"),
                ("/part-cross-origin", b"part"),
            ],
            self.storage_server.received_bodies,
        )
        self.assertEqual(
            ["/api/rest/v1/users-cross-origin"],
            [path for path, _body in self.api_server.received_bodies],
        )

    def test_same_origin_redirect_keeps_files_auth_headers(self):
        client = ApiClient()
        client.send_request(
            "GET",
            "/same-origin",
            api_key="testkey",
            workspace_id=123,
            params={},
        )

        redirected_headers = self.api_server.received_headers[0]
        self.assertEqual("testkey", redirected_headers["X-FilesAPI-Key"])
        self.assertEqual("123", redirected_headers["X-Files-Workspace-Id"])


class TestTransferUrlScheme(unittest.TestCase):
    """An API reached over HTTPS names only https:// transfer URLs: a plain
    http:// one, which would carry the file's bytes and the signed URL in
    the clear, is refused before anything is sent to it."""

    def setUp(self):
        self.authority = TestAuthority.create(self)
        self.api = start_loopback_api(self, tls=self.authority)
        self.client = files_sdk.Client(
            api_key="key", base_url=self.api.url, verify=self.authority.ca
        )
        self.addCleanup(self.client.close)

    def send_part(self, storage):
        api_client = ApiClient(Operation.start(self.client))
        return api_client.send_remote_request(
            "PUT", storage.url + "/part", body=b"part"
        )

    def test_a_plain_http_transfer_url_is_refused_when_the_api_is_https(self):
        plain = start_loopback_api(self)
        secure = start_loopback_api(self, tls=self.authority)
        secure.reply(200)

        with self.assertRaises(APIConnectionError) as caught:
            self.send_part(plain)
        self.assertIn("not https://", str(caught.exception))
        self.assertEqual(200, self.send_part(secure).status_code)

        self.assertEqual([], plain.requests)
        self.assertEqual(1, len(secure.requests))
        self.assertEqual([], self.api.requests)


if __name__ == "__main__":
    unittest.main()

import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import files_sdk
from files_sdk.api_client import ApiClient


class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/rest/v1/cross-origin":
            self.send_response(302)
            self.send_header("Location", self.server.cross_origin_url + "/download")
            self.end_headers()
            return
        if self.path == "/api/rest/v1/same-origin":
            self.send_response(302)
            self.send_header("Location", "/api/rest/v1/final")
            self.end_headers()
            return

        self.server.received_headers.append(self.headers)
        self.send_response(204)
        self.end_headers()

    def log_message(self, *args):
        pass


class TestRedirectAuth(unittest.TestCase):
    def setUp(self):
        self.api_server = ThreadingHTTPServer(("127.0.0.1", 0), RedirectHandler)
        self.storage_server = ThreadingHTTPServer(("127.0.0.1", 0), RedirectHandler)
        self.api_server.received_headers = []
        self.storage_server.received_headers = []
        self.api_url = "http://127.0.0.1:{}".format(self.api_server.server_port)
        self.storage_url = "http://127.0.0.1:{}".format(
            self.storage_server.server_port
        )
        self.api_server.cross_origin_url = self.storage_url
        self.storage_server.cross_origin_url = self.api_url
        self.threads = [
            threading.Thread(target=self.api_server.serve_forever),
            threading.Thread(target=self.storage_server.serve_forever),
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


if __name__ == "__main__":
    unittest.main()

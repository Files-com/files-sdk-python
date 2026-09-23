import io
import json
import logging
import socket
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import files_sdk
from files_sdk.api_client import ApiClient
from files_sdk.error import APIConnectionError, APIError, NotFoundError


class TransferHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        self.rfile.read(int(self.headers.get("Content-Length", 0)))
        self.do_GET()

    def do_GET(self):
        self.server.requests += 1
        if self.path.startswith("/disconnect"):
            self.connection.shutdown(socket.SHUT_RDWR)
            self.connection.close()
            return
        body = self.path.encode()
        status = 403 if self.path.startswith("/denied") else 200
        if self.path.startswith("/typed"):
            status = 404
            body = json.dumps({"type": "not-found", "error": self.path}).encode()
        self.send_response(status)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


class TestTransferPrivacy(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), TransferHandler)
        self.server.requests = 0
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.addCleanup(self.thread.join)
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        for name, value in {
            "max_network_retries": 2,
            "initial_network_retry_delay": 0,
            "max_network_retry_delay": 0,
            "console_log_level": "",
        }.items():
            patcher = patch.object(files_sdk, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def url(self, path):
        return "http://127.0.0.1:{}/{}?X-Amz-Credential=private-credential&X-Amz-Signature=private-signature".format(
            self.server.server_port, path
        )

    def assert_safe(self, text):
        for secret in ("127.0.0.1", "X-Amz", "private-credential", "private-signature"):
            self.assertNotIn(secret, text)

    def test_transfer_failures_keep_urls_out_of_logs_and_error_text(self):
        for download in (False, True):
            for path, error_type in (("disconnect", APIConnectionError), ("denied", APIError)):
                with self.subTest(download=download, path=path):
                    with self.assertLogs("files_sdk", level=logging.DEBUG) as logs:
                        with self.assertRaises(error_type) as caught:
                            if download:
                                ApiClient().stream_download(self.url(path), io.BytesIO())
                            else:
                                ApiClient().send_remote_request("PUT", self.url(path), body=b"part")
                    self.assert_safe(str(caught.exception))
                    self.assert_safe("\n".join(record.getMessage() for record in logs.records if record.levelno > logging.DEBUG))
                    self.assertIn("private-signature", "\n".join(logs.output))
                    if path == "denied":
                        self.assertEqual(caught.exception.http_status, 403)
        self.assertEqual(self.server.requests, 6)

    def test_successful_upload_does_not_log_the_transfer_url_at_info(self):
        with self.assertLogs("files_sdk", level=logging.INFO) as logs:
            response = ApiClient().send_remote_request("PUT", self.url("upload"), body=b"part")
        self.assertEqual(response.status_code, 200)
        self.assert_safe("\n".join(logs.output))

    def test_transfer_api_errors_keep_their_type_without_echoing_the_url(self):
        with self.assertLogs("files_sdk", level=logging.INFO) as logs:
            with self.assertRaises(NotFoundError) as caught:
                ApiClient().send_remote_request("PUT", self.url("typed"), body=b"part")
        self.assertEqual(caught.exception.http_status, 404)
        self.assert_safe(str(caught.exception))
        self.assert_safe("\n".join(logs.output))

import io
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import files_sdk
from files_sdk.api_client import ApiClient


class DownloadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        chunk = b"\x00\xff" * 4096
        try:
            if self.path == "/stall-headers":
                self.server.release_response.wait(5)
            self.send_response(200)
            if self.path == "/incomplete-body":
                self.send_header("Transfer-Encoding", "chunked")
            else:
                self.send_header("Content-Length", str(len(chunk) * 3))
            self.end_headers()
            if self.path == "/incomplete-body":
                self.wfile.write(b"%x\r\n" % len(chunk) + chunk + b"\r\n")
                self.wfile.flush()
                return  # Close without the final chunk.
            if self.path == "/stall-body":
                self.server.release_response.wait(5)
            for _ in range(3):
                self.wfile.write(chunk)
                self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def log_message(self, *args):
        pass


class TestStreamDownload(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), DownloadHandler)
        self.server.release_response = threading.Event()
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.url = "http://127.0.0.1:{}".format(self.server.server_port)

    def tearDown(self):
        self.server.release_response.set()
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()

    @patch.object(files_sdk, "read_timeout", 0.2)
    def test_stalled_download_raises_a_network_error(self):
        for path in ("/stall-headers", "/stall-body"):
            with self.subTest(path=path):
                with self.assertRaises(files_sdk.error.APIConnectionError):
                    ApiClient().stream_download(self.url + path, io.BytesIO())

    def test_download_preserves_binary_content(self):
        output = io.BytesIO()
        ApiClient().stream_download(self.url + "/stream", output)
        self.assertEqual(output.getvalue(), b"\x00\xff" * 4096 * 3)

    def test_interrupted_download_raises_a_network_error(self):
        output = io.BytesIO()
        with self.assertRaises(files_sdk.error.APIConnectionError):
            ApiClient().stream_download(self.url + "/incomplete-body", output)
        self.assertEqual(output.getvalue(), b"\x00\xff" * 4096)


if __name__ == "__main__":
    unittest.main()

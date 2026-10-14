import gzip
import io
import threading
import tracemalloc
import unittest
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import files_sdk
from files_sdk.api_client import ApiClient

# Decodes to 64 KiB, several of the SDK's 8 KiB reads.
CONTENT = bytes(range(256)) * 256

# Chunked responses with a Content-Encoding: path -> (encoding, body).
ENCODED_RESPONSES = {
    "/gzip": ("gzip", gzip.compress(CONTENT)),
    "/deflate": ("deflate", zlib.compress(CONTENT)),
    # urllib3 2.6.2 through 2.7.0 looped forever on bytes after the end of
    # a Deflate stream (GHSA-gh4c-6fx4-qh6g).
    "/deflate-trailing-bytes": ("deflate", zlib.compress(CONTENT) + b"extra"),
    "/corrupt-gzip": ("gzip", gzip.compress(CONTENT)[:40] + b"not gzip" * 64),
}


class DownloadHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        chunk = b"\x00\xff" * 4096
        try:
            if self.path in ENCODED_RESPONSES:
                encoding, body = ENCODED_RESPONSES[self.path]
                self.send_response(200)
                self.send_header("Content-Encoding", encoding)
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                self.wfile.write(b"%x\r\n%s\r\n0\r\n\r\n" % (len(body), body))
                return
            if self.path == "/endless-chunk-size":
                # A chunk-size line that never ends: 16 MiB without a newline.
                self.send_response(200)
                self.send_header("Transfer-Encoding", "chunked")
                self.end_headers()
                run = b"f" * 2**20
                for _ in range(16):
                    self.wfile.write(run)
                return
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
        except ConnectionError:  # The client stopped reading.
            pass

    def log_message(self, *args):
        pass


class TestStreamDownload(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), DownloadHandler)
        self.server.release_response = threading.Event()
        self.thread = threading.Thread(
            target=self.server.serve_forever, kwargs={"poll_interval": 0.005}
        )
        self.thread.start()
        self.url = "http://127.0.0.1:{}".format(self.server.server_port)
        # The module facade's transfers: a plain-HTTP API, like the stand-in.
        patcher = patch.object(files_sdk, "base_url", "http://localhost:4042")
        patcher.start()
        self.addCleanup(patcher.stop)

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

    def test_compressed_downloads_are_decoded(self):
        for path in ("/gzip", "/deflate"):
            with self.subTest(path=path):
                output = io.BytesIO()
                ApiClient().stream_download(self.url + path, output)
                self.assertEqual(output.getvalue(), CONTENT)

    def test_bytes_after_a_deflate_stream_do_not_stall_the_download(self):
        # A read timeout cannot interrupt a decoder that loops without
        # reading, so bound the download here instead. The daemon thread
        # cannot hold up the test run; its exception, if any, fails the test.
        output = io.BytesIO()
        failures = []

        def download():
            try:
                ApiClient().stream_download(
                    self.url + "/deflate-trailing-bytes", output
                )
            except BaseException as error:
                failures.append(error)

        worker = threading.Thread(target=download, daemon=True)
        worker.start()
        worker.join(10)
        self.assertFalse(worker.is_alive(), "The download did not finish.")
        if failures:
            raise failures[0]
        self.assertEqual(output.getvalue(), CONTENT)

    def test_a_corrupt_compressed_download_raises_a_network_error(self):
        with self.assertRaises(files_sdk.error.APIConnectionError):
            ApiClient().stream_download(
                self.url + "/corrupt-gzip", io.BytesIO()
            )

    def test_a_download_url_requests_cannot_use_raises_a_network_error(self):
        # An invalid hostname label, as a malformed transfer URL could have.
        url = "http://" + "\u0660" * 300 + ".example/object"
        with self.assertRaises(files_sdk.error.APIConnectionError):
            ApiClient().stream_download(url, io.BytesIO())

    def test_an_endless_chunk_size_line_fails_without_buffering_it(self):
        # urllib3 before 2.8.0 buffered the whole line (GHSA-vxq7-64xx-v4gw).
        tracemalloc.start()
        try:
            with self.assertRaises(files_sdk.error.APIConnectionError):
                ApiClient().stream_download(
                    self.url + "/endless-chunk-size", io.BytesIO()
                )
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
        self.assertLess(peak, 8 * 2**20)

    def test_file_close_releases_its_read_buffer(self):
        with self.subTest("explicit close after a complete read"):
            f = files_sdk.file.open("remote.bin", "rb")
            f.download_uri = self.url + "/stream"
            self.assertEqual(f.read(), b"\x00\xff" * 4096 * 3)
            f.close()
            self.assertTrue(f.closed)
            self.assertTrue(f.io_obj.closed)

        with self.subTest("context exit after an interrupted read"):
            f = files_sdk.file.open("remote.bin", "rb")
            f.download_uri = self.url + "/incomplete-body"
            with self.assertRaises(files_sdk.error.APIConnectionError):
                with f:
                    f.read()
            self.assertTrue(f.closed)
            self.assertTrue(f.io_obj.closed)


if __name__ == "__main__":
    unittest.main()

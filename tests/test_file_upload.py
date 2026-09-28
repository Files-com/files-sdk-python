import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

import files_sdk
from files_sdk.error import APIError

PAYLOAD = b"\x00\xff\r\n" * 2048


class UploadHandler(BaseHTTPRequestHandler):
    def do_PUT(self):
        self.server.uploads.append(self.rfile.read(int(self.headers["Content-Length"])))
        self.send_response(200)
        self.send_header("ETag", '"part-etag"')
        self.send_header("Content-Length", "0")
        self.end_headers()

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if "/file_actions/begin_upload/" in self.path:
            self.respond(200, [{
                "upload_uri": "http://127.0.0.1:{}/upload".format(self.server.server_port),
                "http_method": "PUT",
                "partsize": 1024 * 1024,
                "ref": "upload-ref",
                "part_number": 1,
            }])
        elif self.server.fail_finalization:
            self.respond(503, {"error": "Finalization failed", "type": "service-unavailable"})
        else:
            self.server.finalizations.append((body, self.headers["X-FilesAPI-Key"]))
            self.respond(200, {"path": body["path"], "size": body["size"], "type": "file"})

    def respond(self, status, data):
        encoded = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *args):
        pass


class TestFileUpload(unittest.TestCase):
    def setUp(self):
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), UploadHandler)
        self.server.uploads = []
        self.server.finalizations = []
        self.server.fail_finalization = False
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.addCleanup(self.thread.join)
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        base_url = "http://127.0.0.1:{}".format(self.server.server_port)
        for name, value in {"base_url": base_url, "max_network_retries": 1}.items():
            patcher = patch.object(files_sdk, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)

    def open_with_payload(self):
        f = files_sdk.file.open("remote.bin", "wb", {"api_key": "optionsKey"})
        f.write(PAYLOAD)
        return f

    def test_close_finalizes_once_and_releases_the_write_buffer(self):
        f = self.open_with_payload()
        write_buffer = f.io_obj

        f.close()
        f.close()

        self.assertEqual(self.server.uploads, [PAYLOAD])
        self.assertEqual(len(self.server.finalizations), 1)
        finalization, api_key = self.server.finalizations[0]
        self.assertEqual(finalization["action"], "end")
        self.assertEqual(finalization["ref"], "upload-ref")
        self.assertEqual(finalization["etags"], [{"etag": "part-etag", "part": 1}])
        self.assertEqual(finalization["size"], len(PAYLOAD))
        self.assertEqual(api_key, "optionsKey")
        self.assertEqual(f.size, len(PAYLOAD))
        self.assertTrue(f.closed)
        self.assertTrue(write_buffer.closed)
        self.assertTrue(f.io_obj.closed)

    def test_failed_finalization_leaves_the_file_open_with_its_data(self):
        self.server.fail_finalization = True
        f = self.open_with_payload()

        with self.assertRaises(APIError):
            f.close()

        self.assertFalse(f.closed)
        self.assertEqual(f.io_obj.getvalue(), PAYLOAD)


if __name__ == "__main__":
    unittest.main()

import io
import os
import tempfile
import unittest
import warnings
from pathlib import Path

import files_sdk
from files_sdk.error import InvalidParameterError
from files_sdk.models import file
from tests.loopback_api import serve_loopback_api


class NoDataReadyStream(io.RawIOBase):
    """A non-blocking stream that is still open but has no data yet."""

    def readable(self):
        return True

    def readinto(self, buffer):
        return None


class TestUploadSources(unittest.TestCase):
    def reply_with_one_part(self, api, partsize):
        api.reply_json(
            [
                {
                    "ref": "upload-ref",
                    "part_number": 1,
                    "partsize": partsize,
                    "http_method": "PUT",
                    "upload_uri": api.url + "/part-1",
                }
            ]
        )

    def test_uploading_a_file_sends_its_bytes_and_modification_time(self):
        api = serve_loopback_api(self)
        self.reply_with_one_part(api, 5 * 1024 * 1024)
        api.reply(200, headers={"ETag": '"etag-1"'})
        api.reply_json({"path": "reports/data.bin"})
        content = bytes(range(256)) * 3

        with tempfile.TemporaryDirectory() as scratch:
            local = Path(scratch, "data.bin")
            local.write_bytes(content)
            os.utime(local, (0, 1790319948.25))
            with warnings.catch_warnings():
                warnings.simplefilter("error", DeprecationWarning)
                files_sdk.upload_file(str(local), "reports/data.bin")

        begin, part, finish = api.requests
        self.assertEqual(
            begin.path, "/file_actions/begin_upload/reports%2Fdata.bin"
        )
        self.assertEqual((part.method, part.body), ("PUT", content))
        self.assertEqual(finish.path, "/files/reports%2Fdata.bin")
        self.assertEqual(
            finish.json,
            {
                "action": "end",
                "etags": [{"etag": "etag-1", "part": 1}],
                "path": "reports/data.bin",
                # The modification time in UTC, without an offset.
                "provided_mtime": "2026-09-25T07:05:48.250000",
                "ref": "upload-ref",
                "size": len(content),
            },
        )

    def test_a_stream_with_no_data_ready_stops_before_sending_a_part(self):
        api = serve_loopback_api(self)
        self.reply_with_one_part(api, 5)
        stream = NoDataReadyStream()

        with self.assertRaises(InvalidParameterError) as caught:
            file.upload_chunks(stream, "reports/a.txt", {})

        self.assertIn("read() returned None", str(caught.exception))
        # Only the part was requested: nothing was sent to it and the upload
        # was not completed. The caller's stream is left open.
        self.assertEqual(
            [(request.method, request.path) for request in api.requests],
            [("POST", "/file_actions/begin_upload/reports%2Fa.txt")],
        )
        self.assertFalse(stream.closed)

    def test_closing_a_file_object_uploads_what_was_written_and_releases_it(
        self,
    ):
        api = serve_loopback_api(self)
        self.reply_with_one_part(api, 1024)
        api.reply(200, headers={"ETag": '"etag-1"'})
        api.reply_json({"path": "notes.txt", "size": 5})

        with files_sdk.open("notes.txt", "wb") as remote:
            remote.write(b"hello")
            buffer = remote.io_obj

        begin, part, finish = api.requests
        self.assertEqual((part.method, part.body), ("PUT", b"hello"))
        self.assertEqual("end", finish.json["action"])
        self.assertTrue(buffer.closed)
        self.assertTrue(remote.io_obj.closed)
        with self.assertRaises(OSError):
            remote.write(b"more")

    def test_closing_a_file_read_releases_its_downloaded_content(self):
        api = serve_loopback_api(self)
        api.reply_json(
            {
                "path": "notes.txt",
                "download_uri": api.url + "/storage/notes.txt",
            }
        )
        api.reply(200, b"remote content")

        remote = files_sdk.open("notes.txt", "rb")
        self.assertEqual(b"remote content", remote.read())
        remote.close()

        self.assertTrue(remote.io_obj.closed)
        with self.assertRaises(OSError):
            remote.read()


if __name__ == "__main__":
    unittest.main()

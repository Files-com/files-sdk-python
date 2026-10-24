import io
import os
import sys
import tempfile
import threading
import time
import unittest
import warnings
from pathlib import Path
from unittest import mock

import files_sdk
from files_sdk.error import InvalidParameterError, InvalidRequestError
from files_sdk.models import file
from tests.loopback_api import serve_loopback_api
from tests.upload_fixtures import UploadService


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

    def test_a_file_edited_after_it_was_created_uploads_read_whole_or_as_sent(
        self,
    ):
        # Edited and closed a moment after it was created, as a person edits
        # a file, so that Windows records its creation and its last change
        # apart. A part of up to 64 KiB is read whole before it is sent; a
        # larger one is read from the file as it is sent.
        for content in (bytes(range(256)) * 3, bytes(range(256)) * 256 + b"!"):
            with self.subTest(size=len(content)):
                api = serve_loopback_api(self)
                self.reply_with_one_part(api, 5 * 1024 * 1024)
                api.reply(200, headers={"ETag": '"etag-1"'})
                api.reply_json({"path": "reports/data.bin"})
                with tempfile.TemporaryDirectory() as scratch:
                    local = Path(scratch, "data.bin")
                    local.write_bytes(bytes(len(content)))
                    time.sleep(0.05)
                    with open(local, "r+b") as edited:
                        edited.write(content)

                    uploaded = files_sdk.upload_file(
                        str(local), "reports/data.bin"
                    )

                # One request for the part, its bytes exactly, and one
                # completion.
                begin, part, finish = api.requests
                self.assertEqual(
                    "/file_actions/begin_upload/reports%2Fdata.bin", begin.path
                )
                self.assertEqual(("PUT", content), (part.method, part.body))
                self.assertEqual("/files/reports%2Fdata.bin", finish.path)
                self.assertEqual(
                    ("end", [{"etag": "etag-1", "part": 1}], len(content)),
                    (
                        finish.json["action"],
                        finish.json["etags"],
                        finish.json["size"],
                    ),
                )
                self.assertEqual("reports/data.bin", uploaded.path)

    def test_a_write_through_a_handle_kept_open_fails_the_upload_before_it_completes(
        self,
    ):
        # The writer's handle stays open and has written before the upload,
        # so its write during the upload can leave the file's size, times
        # and identity all as they were, as Windows can: there only notice of
        # the write itself shows it. The part read before is sent, the one
        # after is not read, and nothing is completed.
        service = UploadService(
            self, part_size=4, grant={"parallel_parts": False}
        )
        client = files_sdk.Client(
            api_key="key", base_url=service.url, initial_network_retry_delay=0
        )
        self.addCleanup(client.close)
        with tempfile.TemporaryDirectory() as scratch:
            local = Path(scratch, "data.bin")
            local.write_bytes(b"abcdefgh")
            with open(local, "r+b", buffering=0) as writer:
                writer.write(b"abcdefgh")

                def write_once_part_one_arrives(number):
                    if number == 1:
                        writer.seek(0)
                        writer.write(b"ABCDEFGH")

                service.on_put = write_once_part_one_arrives
                with self.assertRaises(InvalidRequestError) as caught:
                    client.file.upload_file(local, "a.bin")
        self.assertIn(
            "changed while it was being uploaded", str(caught.exception)
        )
        self.assertEqual(
            [b"abcd"],
            [part.body for parts in service.stored.values() for part in parts],
        )
        self.assertEqual([], service.finishes)

    @unittest.skipUnless(sys.platform == "win32", "Windows' notice of writes")
    def test_a_file_windows_gives_no_notice_of_writes_for_still_uploads(self):
        # Windows refuses the notice, as while another handle locks a byte
        # range of the file; or the file is on no local disk, where none is
        # asked for. Either way the upload goes on, checked by the file's
        # metadata alone.
        if sys.platform != "win32":
            # skipUnless does not keep a type checker out of the rest; this does.
            raise AssertionError("Only Windows gives notice of writes")
        import contextlib
        import ctypes

        from files_sdk import windows_file

        bound = windows_file._api()
        assert bound is not None
        asked = []

        def refused(handle, code, *rest):
            asked.append(code)
            ctypes.set_last_error(300)  # ERROR_OPLOCK_NOT_GRANTED
            return False

        content = bytes(range(256)) * 3
        for case, drive in (("not granted", None), ("not on a local disk", 4)):
            with self.subTest(case):
                asked.clear()
                api = serve_loopback_api(self)
                self.reply_with_one_part(api, 5 * 1024 * 1024)
                api.reply(200, headers={"ETag": '"etag-1"'})
                api.reply_json({"path": "reports/data.bin"})
                with tempfile.TemporaryDirectory() as scratch:
                    local = Path(scratch, "data.bin")
                    local.write_bytes(content)
                    with contextlib.ExitStack() as patches:
                        patches.enter_context(
                            mock.patch.object(
                                bound, "DeviceIoControl", refused
                            )
                        )
                        if drive is not None:
                            patches.enter_context(
                                mock.patch.object(
                                    bound, "GetDriveTypeW", lambda root: drive
                                )
                            )  # DRIVE_REMOTE
                        uploaded = files_sdk.upload_file(
                            str(local), "reports/data.bin"
                        )

                begin, part, finish = api.requests
                self.assertEqual(("PUT", content), (part.method, part.body))
                self.assertEqual(
                    ("end", len(content)),
                    (finish.json["action"], finish.json["size"]),
                )
                self.assertEqual("reports/data.bin", uploaded.path)
                # Only a file on a local disk is asked about.
                self.assertEqual(1 if drive is None else 0, len(asked))

    @unittest.skipUnless(sys.platform == "win32", "Windows' notice of writes")
    def test_an_upload_refused_before_it_begins_lets_go_of_its_file(self):
        # Asking for notice of writes holds a handle to the file from the
        # start: an upload stopped by its own checks before it begins
        # releases it too.
        api = serve_loopback_api(self)
        with tempfile.TemporaryDirectory() as scratch:
            local = Path(scratch, "data.bin")
            local.write_bytes(b"abcdefgh")
            with self.assertRaisesRegex(
                InvalidParameterError, "The SDK sets ref"
            ):
                files_sdk.upload_file(
                    str(local), "a.bin", params={"ref": "other"}
                )
            with self.assertRaisesRegex(
                InvalidParameterError, "file of its own"
            ):
                files_sdk.upload_file(
                    str(local), "a.bin", checkpoint=str(local)
                )
            self.assertTrue(self.opened_alone(local))
        self.assertEqual([], api.requests)

    @unittest.skipUnless(sys.platform == "win32", "Windows' notice of writes")
    def test_a_notice_windows_finishes_late_lets_go_of_its_file_while_many_more_stay_unfinished(
        self,
    ):
        # Closing a guard asks Windows to cancel its request, which Windows
        # can finish only later; until it has, the SDK keeps the guard. Here
        # Windows takes every request and finishes none when asked to cancel
        # it, so 63 guards stay unfinished: as many as one wait can watch
        # beside the SDK's own event. Then Windows finishes the request of
        # one guard more, and no guard is closed after it: that guard still
        # lets go of its file, and the others keep theirs.
        if sys.platform != "win32":
            raise AssertionError("Only Windows gives notice of writes")
        import ctypes

        from files_sdk import windows_file

        bound = windows_file._api()
        assert bound is not None
        real_wait = bound.WaitForMultipleObjects
        gate, settled = threading.Event(), threading.Event()
        waits = []

        def taken(handle, code, *rest):
            # Windows holds the request: STATUS_PENDING, and ERROR_IO_PENDING.
            rest[-1]._obj.Internal = 0x103
            ctypes.set_last_error(997)
            return False

        def wait(*arguments):
            # The SDK's first wait goes ahead once every guard is closed; the
            # next follows its look at all of them.
            waits.append(arguments[0])
            if len(waits) == 1:
                gate.wait(10)
            else:
                settled.set()
            return real_wait(*arguments)

        def finish(guard):
            # As Windows finishes a cancelled request, though its event is
            # set first here, so never once the guard may be released.
            event = guard._event
            if event is not None:
                bound.SetEvent(event)
            guard._overlapped.Internal = 0xC0000120  # STATUS_CANCELLED

        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        held, late = Path(scratch.name, "held.bin"), Path(
            scratch.name, "late.bin"
        )
        held.write_bytes(b"held")
        late.write_bytes(b"late")
        guards = []

        def finish_all():
            # Windows finishes the rest at last, before their files are removed.
            for guard in guards:
                finish(guard)
            self.opened_alone(held)

        self.addCleanup(finish_all)
        self.addCleanup(gate.set)
        with mock.patch.multiple(
            bound, DeviceIoControl=taken, WaitForMultipleObjects=wait
        ):
            for path in [held] * 63 + [late]:
                guard = windows_file.acquire(str(path))
                self.assertIsNotNone(guard)
                assert guard is not None
                guards.append(guard)
                guard.close()
            gate.set()
            self.assertTrue(settled.wait(10))
            finish(guards[-1])
            self.assertTrue(self.opened_alone(late))
            self.assertFalse(self.opened_alone(held, seconds=0))

    def opened_alone(self, path, seconds=5):
        """Whether path can be opened sharing nothing, as only a file no
        handle is open to can: waiting up to seconds, for a request Windows
        may finish only after the upload has returned."""
        if sys.platform != "win32":
            raise AssertionError(
                "Only Windows opens a file sharing nothing this way"
            )
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel32.CreateFileW.restype = wintypes.HANDLE
        kernel32.CreateFileW.argtypes = (
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        )
        kernel32.CloseHandle.argtypes = (wintypes.HANDLE,)
        deadline = time.monotonic() + seconds
        while True:
            # GENERIC_READ, sharing nothing, OPEN_EXISTING.
            handle = kernel32.CreateFileW(
                str(path), 0x80000000, 0, None, 3, 0, None
            )
            if handle not in (None, ctypes.c_void_p(-1).value):
                kernel32.CloseHandle(handle)
                return True
            if time.monotonic() >= deadline:
                return False
            time.sleep(0.05)

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

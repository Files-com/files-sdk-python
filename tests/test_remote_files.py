import io
import random
import unittest
from unittest import mock

import files_sdk
from files_sdk.error import (
    APIConnectionError,
    InvalidRequestError,
    OperationCancelledError,
)
from tests.download_fixtures import DownloadService
from tests.upload_fixtures import UploadService

RANGE = 1000


def content(size, seed=1):
    return random.Random(seed).randbytes(size)


class RemoteFileTestCase(unittest.TestCase):
    def setUp(self):
        patch = mock.patch("files_sdk.download.READ_RANGE_SIZE", RANGE)
        patch.start()
        self.addCleanup(patch.stop)

    def client(self, service, **settings):
        client = files_sdk.Client(
            api_key="key",
            base_url=service.url,
            initial_network_retry_delay=0,
            **settings,
        )
        self.addCleanup(client.close)
        return client


class TestReadingRemoteFiles(RemoteFileTestCase):
    def test_a_binary_file_streams_a_range_at_a_time_as_reads_need_it(self):
        data = content(4500)
        service = DownloadService(self, data)
        with self.client(service).file.open("big.bin", "rb") as remote:
            first = remote.read(300)
            self.assertEqual(service.ranges(), ["bytes=0-999"])
            buffer = bytearray(900)
            count = remote.readinto(buffer)
            rest = remote.read()
            self.assertEqual(remote.read(), b"")
        self.assertEqual(first + bytes(buffer[:count]) + rest, data)
        # Ranges of the version, which is 4500 bytes, with its If-Match.
        self.assertEqual(
            service.ranges(),
            [
                "bytes={}-{}".format(s, min(s + RANGE, 4500) - 1)
                for s in range(0, 4500, RANGE)
            ],
        )
        self.assertEqual(
            {r["encoding"] for r in service.storage_requests()}, {"identity"}
        )
        self.assertEqual(
            {r["if_match"] for r in service.storage_requests()}, {service.etag}
        )

    def test_lines_are_read_one_at_a_time_in_either_mode(self):
        text = "".join("line {} é€\r\n".format(i) for i in range(300))
        service = DownloadService(self, text.encode("utf-8"))
        with self.client(service).file.open("t.txt", "r") as remote:
            lines = list(remote)
        self.assertEqual("".join(lines), text)
        self.assertEqual(lines[0], "line 0 é€\r\n")
        with self.client(service).file.open("t.txt", "rb") as remote:
            self.assertEqual(
                remote.readline(), "line 0 é€\r\n".encode("utf-8")
            )
            self.assertEqual(len(remote.readlines()), 299)

    def test_text_is_decoded_across_ranges_with_its_line_endings_kept(self):
        text = "é€\r\n" * 700
        service = DownloadService(self, text.encode("utf-8"))
        with self.client(service).file.open("t.txt") as remote:
            self.assertEqual(remote.read(5), text[:5])
            self.assertEqual(remote.readall(), text[5:])

    def test_storage_that_ignores_ranges_is_refused_for_an_identified_version(
        self,
    ):
        service = DownloadService(self, content(4500))
        service.ignore_ranges = True
        with self.client(service).file.open("big.bin", "rb") as remote:
            with self.assertRaisesRegex(
                APIConnectionError, "bytes 0-999 was answered with HTTP 200"
            ):
                remote.read(10)

    def test_a_file_without_a_download_identity_is_read_from_one_whole_answer(
        self,
    ):
        data = content(4500)
        for label, switch in (
            ("absent", "absent"),
            ("unavailable", "unavailable"),
        ):
            with self.subTest(label):
                service = DownloadService(self, data)
                service.identity = switch
                # The file changes after the first answer; nothing after it is read.
                service.change_after = (1, content(4500, seed=2))
                with self.client(service).file.open("big.bin", "rb") as remote:
                    self.assertEqual(remote.read(10), data[:10])
                    self.assertEqual(remote.read(), data[10:])
                self.assertEqual(service.ranges(), [None])

    def test_the_size_is_what_storage_states_once_reading_starts(self):
        # Files.com's record says 99999 bytes; storage serves 4500. The size
        # is unknown, not 0, until a read has asked storage for the file.
        data = content(4500)
        for label, identity in (
            ("ranges of an identified version", "if-match"),
            ("one whole answer", "absent"),
        ):
            with self.subTest(label):
                service = DownloadService(self, data, reported_size=99999)
                service.identity = identity
                with self.client(service).file.open("big.bin", "rb") as remote:
                    self.assertIsNone(remote.size)
                    self.assertEqual(remote.read(10), data[:10])
                    self.assertEqual(4500, remote.size)

    def test_the_size_stays_unknown_when_storage_states_none_to_trust(self):
        # An encoded answer's Content-Length is the encoding's, and an unsized
        # answer has none: the size is None, not the record's.
        data = b"compressible " * 400
        for label, switch, value in (
            ("encoded", "gzip", "whole"),
            ("unsized", "whole_unsized", "full"),
        ):
            with self.subTest(label):
                service = DownloadService(self, data)
                service.identity = "absent"
                setattr(service, switch, value)
                with self.client(service).file.open("a.txt", "rb") as remote:
                    self.assertEqual(remote.read(), data)
                    self.assertIsNone(remote.size)

    def test_an_empty_file_reads_as_empty(self):
        for identity in ("if-match", "absent"):
            with self.subTest(identity=identity):
                service = DownloadService(self, b"")
                service.identity = identity
                with self.client(service).file.open("e.bin", "rb") as remote:
                    self.assertEqual(remote.read(), b"")
                    # Known to be empty, which is not unknown.
                    self.assertEqual(0, remote.size)
                with self.client(service).file.open("e.txt") as remote:
                    self.assertEqual(remote.read(), "")

    def test_a_file_that_changes_while_it_is_read_raises(self):
        service = DownloadService(self, content(4500, seed=1))
        service.change_after = (2, content(4500, seed=2))
        with self.client(service).file.open("big.bin", "rb") as remote:
            remote.read(1500)
            with self.assertRaisesRegex(
                InvalidRequestError, "changed while it was being downloaded"
            ):
                remote.read()

    def test_an_expired_url_is_renewed_between_ranges(self):
        data = content(3500)
        # A renewal brings Files.com's record again, whose size is wrong.
        service = DownloadService(self, data, reported_size=99999)
        service.expire_first_url = 2
        with self.client(service).file.open("big.bin", "rb") as remote:
            self.assertEqual(remote.read(), data)
            self.assertEqual(3500, remote.size)
        self.assertEqual(service.issued, 2)

    def test_the_web_app_answering_raises_before_anything_is_returned(self):
        service = DownloadService(self, content(100))
        service.frontend = True
        with self.client(service).file.open("a.bin", "rb") as remote:
            with self.assertRaisesRegex(APIConnectionError, "web app"):
                remote.read()

    def test_cancelling_stops_reading(self):
        service = DownloadService(self, content(4500))
        token = files_sdk.CancellationToken()
        with self.client(service).file.open(
            "a.bin", "rb", {"cancel_token": token}
        ) as remote:
            remote.read(100)
            token.cancel()
            with self.assertRaises(OperationCancelledError):
                remote.read()


class TestRemoteFileContract(RemoteFileTestCase):
    def test_operations_a_remote_file_cannot_do_raise_unsupported_operation(
        self,
    ):
        service = DownloadService(self, content(100))
        with self.client(service).file.open("a.bin", "rb") as remote:
            self.assertFalse(remote.seekable())
            self.assertTrue(remote.readable())
            self.assertFalse(remote.writable())
            for call in (
                lambda: remote.seek(0),
                remote.tell,
                remote.truncate,
                remote.fileno,
                lambda: remote.write(b"x"),
            ):
                with self.assertRaises(io.UnsupportedOperation):
                    call()
        with self.client(service).file.open("a.txt", "r") as remote:
            with self.assertRaises(io.UnsupportedOperation):
                remote.readinto(bytearray(4))

    def test_modes_other_than_read_and_write_are_refused_before_any_request(
        self,
    ):
        service = DownloadService(self, content(100))
        client = self.client(service)
        for mode in ("a", "ab", "x", "r+", "w+b"):
            with self.subTest(mode=mode):
                with self.assertRaises(io.UnsupportedOperation):
                    client.file.open("a.bin", mode)
        for mode in ("", "q", "rw", "rbt", "rr", 3):
            with self.subTest(mode=mode):
                with self.assertRaises(ValueError):
                    client.file.open("a.bin", mode)  # type: ignore[arg-type]
        self.assertEqual(service.requests, [])

    def test_a_closed_file_raises_as_io_and_version_1_did(self):
        service = DownloadService(self, content(100))
        remote = self.client(service).file.open("a.bin", "rb")
        remote.close()
        remote.close()
        for call in (remote.read, remote.readline, remote.flush):
            with self.assertRaises(ValueError):
                call()
            with self.assertRaises(OSError):
                call()

    def test_a_file_that_was_not_opened_says_how_to_read_it(self):
        service = DownloadService(self, content(100))
        file = self.client(service).file.new({"path": "a.bin"})
        with self.assertRaisesRegex(io.UnsupportedOperation, "files_sdk.open"):
            file.read()

    def test_writing_sends_parts_and_close_completes_the_upload(self):
        service = UploadService(self, part_size=4)
        remote = self.client(service).file.open("notes.txt", "w")
        self.assertTrue(remote.writable())
        self.assertTrue(remote.writeable())
        self.assertFalse(remote.readable())
        remote.writelines(["héllo", " ", "wörld"])
        with self.assertRaises(io.UnsupportedOperation):
            remote.read()
        remote.flush()
        remote.close()
        self.assertEqual(service.assembled(), "héllo wörld".encode("utf-8"))
        self.assertEqual(remote.path, "notes.txt")
        self.assertFalse(remote.writable())


if __name__ == "__main__":
    unittest.main()

"""Transfer boundaries other SDKs were found to get wrong, run through the
real engines: completeness of every range, whole answers that are only part
of a file, ranges a server stops serving, the temporary file's identity,
folder downloads and links, local files and folders swapped while the SDK
uses them, limiter places given up while waiting, the relocated site on a
refreshed URL, the caller's own stream failures and short writes, part
offsets across continued uploads and renewed grants of serial uploads.

Swaps are scheduled at the real file system calls the SDK makes, by
running the interfering change just before the SDK's call proceeds; the
SDK's own behavior is not replaced."""

import io
import os
import random
import stat
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

import requests

import files_sdk
from files_sdk.api_client import ApiClient
from files_sdk.error import (
    APIConnectionError,
    InvalidParameterError,
    InvalidRequestError,
    OperationCancelledError,
)
from files_sdk.models.file_upload_part import FileUploadPart
from tests.download_fixtures import DownloadService, TreeService, sdk_entries
from tests.loopback_api import serve_loopback_api, start_loopback_api
from tests.upload_fixtures import UploadService

RANGE = 1000


def content(size, seed=1):
    return random.Random(seed).randbytes(size)


class BoundaryTestCase(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)
        for name in ("DEFAULT_RANGE_SIZE", "READ_RANGE_SIZE"):
            patch = mock.patch("files_sdk.download." + name, RANGE)
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

    def stages(self):
        return sdk_entries(self.scratch)

    def stage_files(self):
        return [
            name
            for name in self.stages()
            if name.endswith(".files_sdk-download")
        ]


class TestRangeCompleteness(BoundaryTestCase):
    def test_a_range_cut_short_inside_a_well_framed_chunked_body_is_fetched_again(
        self,
    ):
        data = content(5000)
        for destination in ("path", "stream"):
            with self.subTest(destination):
                service = DownloadService(self, data)
                service.chunked_short_once = {2000}
                if destination == "path":
                    self.client(service).file.download_file(
                        "a.bin", self.scratch / "a.bin"
                    )
                    received = (self.scratch / "a.bin").read_bytes()
                else:
                    output = io.BytesIO()
                    self.client(service).file.download_stream("a.bin", output)
                    received = output.getvalue()
                self.assertEqual(received, data)
                self.assertEqual(service.ranges().count("bytes=2000-2999"), 2)

    def test_a_request_for_the_whole_file_answered_with_part_of_it_is_refused(
        self,
    ):
        service = DownloadService(self, content(5000))
        # Without a download identity the file is asked for whole, and that
        # answer is a 206 with half of it.
        service.identity = "absent"
        service.whole_status = 206
        target = self.scratch / "a.bin"
        target.write_bytes(b"previous")
        with self.assertRaisesRegex(
            APIConnectionError, "whole file was answered with HTTP 206"
        ):
            self.client(service).file.download_file("a.bin", target)
        self.assertEqual(target.read_bytes(), b"previous")
        self.assertEqual(self.stages(), [])
        self.assertEqual(service.ranges(), [None])

    def test_a_remote_file_whose_later_range_is_answered_whole_raises_instead_of_returning_the_start(
        self,
    ):
        data = content(3000)
        service = DownloadService(self, data)
        service.ignore_ranges_after = 1
        with self.client(service).file.open("a.bin", "rb") as remote:
            self.assertEqual(remote.read(1000), data[:1000])
            with self.assertRaisesRegex(
                APIConnectionError,
                "bytes 1000-1999 was answered with HTTP 200",
            ):
                remote.read(10)

    def test_the_legacy_stream_download_refuses_part_of_the_file(self):
        api = serve_loopback_api(self)
        api.reply(206, b"abc", {"Content-Range": "bytes 0-2/10"})
        output = io.BytesIO()
        with self.assertRaisesRegex(APIConnectionError, "HTTP 206"):
            ApiClient().stream_download(api.url + "/storage/x", output)
        self.assertEqual(output.getvalue(), b"")


class TestTemporaryFileIdentity(BoundaryTestCase):
    def test_a_replaced_temporary_file_is_never_written_published_or_removed(
        self,
    ):
        service = DownloadService(self, content(5000))
        target = self.scratch / "a.bin"
        target.write_bytes(b"previous")
        moved = self.scratch / "moved-aside"

        def replace_stage(header):
            if header == "bytes=3000-3999":
                [stage] = self.stage_files()
                os.rename(self.scratch / stage, moved)
                (self.scratch / stage).write_bytes(b"FOREIGN")

        service.on_request = replace_stage
        with self.assertRaisesRegex(
            InvalidRequestError, "was replaced by another file"
        ):
            self.client(service).file.download_file(
                "a.bin", target, max_concurrency=1
            )
        [foreign] = self.stage_files()
        self.assertEqual((self.scratch / foreign).read_bytes(), b"FOREIGN")
        self.assertEqual(target.read_bytes(), b"previous")
        self.assertEqual(moved.stat().st_size, 5000)


@unittest.skipIf(sys.platform == "win32", "symbolic links")
class TestFolderDownloadConfinement(BoundaryTestCase):
    def test_a_folder_download_never_writes_through_a_link_as_the_file_or_above_it(
        self,
    ):
        service = TreeService(
            self,
            {
                "docs/leaf.txt": b"remote leaf",
                "docs/sub/deep.txt": b"remote deep",
                "docs/ok.txt": b"ok",
            },
        )
        mirror = self.scratch / "mirror"
        outside = self.scratch / "outside"
        mirror.mkdir()
        outside.mkdir()
        (outside / "victim.txt").write_bytes(b"ORIGINAL")
        (mirror / "leaf.txt").symlink_to(outside / "victim.txt")
        (mirror / "sub").symlink_to(outside, target_is_directory=True)
        result = self.client(service).file.download_directory("docs", mirror)
        self.assertEqual(
            sorted(o.remote_path for o in result.failed),
            ["docs/leaf.txt", "docs/sub/deep.txt"],
        )
        self.assertEqual(sorted(os.listdir(outside)), ["victim.txt"])
        self.assertEqual((outside / "victim.txt").read_bytes(), b"ORIGINAL")
        self.assertTrue((mirror / "leaf.txt").is_symlink())
        self.assertEqual((mirror / "ok.txt").read_bytes(), b"ok")

    def test_a_single_file_download_still_follows_the_link_it_was_given(self):
        service = DownloadService(self, b"remote")
        target = self.scratch / "target.txt"
        target.write_bytes(b"old")
        link = self.scratch / "link.txt"
        link.symlink_to(target)
        self.client(service).file.download_file("a.txt", link)
        self.assertTrue(link.is_symlink())
        self.assertEqual(target.read_bytes(), b"remote")


class TestLimiterPlaces(BoundaryTestCase):
    def test_a_download_cancelled_while_waiting_for_the_limiter_gives_its_place_back(
        self,
    ):
        limiter = files_sdk.TransferLimiter(max_parts=1)
        slow = DownloadService(self, content(500, seed=1))
        started = threading.Event()
        slow.on_request = lambda _header: (started.set(), time.sleep(0.5))
        other = DownloadService(self, content(500, seed=2))
        outcome = {}
        first = threading.Thread(
            target=lambda: outcome.update(
                first=self.client(
                    slow, transfer_limiter=limiter
                ).file.download_stream("a.bin", io.BytesIO())
            )
        )
        first.start()
        self.addCleanup(first.join)
        started.wait(5)
        token = files_sdk.CancellationToken()
        threading.Timer(0.1, token.cancel).start()
        with self.assertRaises(OperationCancelledError):
            self.client(other, transfer_limiter=limiter).file.download_stream(
                "b.bin", io.BytesIO(), {"cancel_token": token}
            )
        self.assertEqual(other.ranges(), [])
        first.join(10)
        self.assertEqual((limiter.parts_in_use, limiter.bytes_in_use), (0, 0))
        output = io.BytesIO()
        self.client(other, transfer_limiter=limiter).file.download_stream(
            "b.bin", output
        )
        self.assertEqual(output.getvalue(), other.content)


class TestRelocatedSite(unittest.TestCase):
    def test_a_refreshed_download_url_and_the_file_keep_the_relocated_site(
        self,
    ):
        issuer = start_loopback_api(self)
        region = start_loopback_api(self)
        pair = [(issuer.url, region.url)]
        issuer.reply_json(
            {
                "type": "not-authenticated/lockout-region-mismatch",
                "http-code": 403,
                "title": "Lockout Region Mismatch",
                "error": "Use another host.",
                "data": {"host": region.url.split("://")[1]},
            },
            status=403,
        )
        region.reply_json(
            {"path": "a.txt", "download_uri": region.url + "/storage/one"}
        )
        region.reply(
            403,
            b"<Error><Code>AccessDenied</Code><Message>Request has expired</Message></Error>",
        )
        region.reply_json(
            {"path": "a.txt", "download_uri": region.url + "/storage/two"}
        )
        region.reply(200, b"content")
        region.reply(204)
        client = files_sdk.Client(
            api_key="devkey",
            base_url=issuer.url,
            region_development_origins=pair,
        )
        self.addCleanup(client.close)
        output = io.BytesIO()
        file = client.file.download_stream("a.txt", output)
        self.assertEqual(output.getvalue(), b"content")
        # Later operations of the file go straight to the region.
        file.delete()
        self.assertEqual(len(issuer.requests), 1)
        self.assertEqual(
            [(r.method, r.url_path.split("/")[-1]) for r in region.requests],
            [
                ("GET", "a.txt"),
                ("GET", "one"),
                ("GET", "a.txt"),
                ("GET", "two"),
                ("DELETE", "a.txt"),
            ],
        )


class TestCallerStreamFailures(BoundaryTestCase):
    class Failing(io.RawIOBase):
        def __init__(self, error):
            self.error = error

        def writable(self):
            return True

        def write(self, data):
            raise self.error

    def test_a_download_stream_that_raises_a_network_looking_error_gets_it_back_unretried(
        self,
    ):
        # Ranges, and a whole file read without a download identity, whose
        # writes happen while its response is read.
        for identity in ("if-match", "absent"):
            with self.subTest(identity=identity):
                mine = requests.exceptions.ConnectionError(
                    "the caller's own socket"
                )
                service = DownloadService(self, content(2500))
                service.identity = identity
                with self.assertRaises(
                    requests.exceptions.ConnectionError
                ) as caught:
                    self.client(service).file.download_stream(
                        "a.bin", self.Failing(mine)
                    )
                self.assertIs(caught.exception, mine)
                # None was fetched again.
                ranges = service.ranges()
                self.assertIn(
                    "bytes=0-999" if identity == "if-match" else None, ranges
                )
                self.assertEqual(len(ranges), len(set(ranges)))

    def test_the_legacy_stream_download_gives_the_callers_error_back_unretried(
        self,
    ):
        api = serve_loopback_api(self, max_network_retries=3)
        api.reply(200, b"data")
        mine = requests.exceptions.ChunkedEncodingError(
            "the caller's own stream"
        )
        with self.assertRaises(
            requests.exceptions.ChunkedEncodingError
        ) as caught:
            ApiClient().stream_download(
                api.url + "/storage/x", self.Failing(mine)
            )
        self.assertIs(caught.exception, mine)
        self.assertEqual(len(api.requests), 1)


class TestContinuedPartOffsets(BoundaryTestCase):
    def service(self):
        return UploadService(
            self,
            part_size=4,
            grant={"part_offset_query": True, "parallel_parts": False},
        )

    def offsets(self, service):
        return [
            (part.number, part.query.get("part_offset"))
            for number in sorted(service.stored)
            for part in service.stored[number]
        ]

    def test_a_continued_upload_keeps_the_upload_s_offsets(self):
        service = self.service()
        files = self.client(service).file
        part, etags, sent = files.upload_chunks(
            io.BytesIO(b"abcdefgh"), "c.bin"
        )
        part, etags, more = files.upload_chunks(
            io.BytesIO(b"ijkl"), "c.bin", part, etags
        )
        self.assertEqual((sent, more), (8, 4))
        self.assertEqual(self.offsets(service), [(1, "0"), (2, "4"), (3, "8")])

    def test_continuing_from_a_part_that_does_not_know_the_offset_sends_nothing(
        self,
    ):
        service = self.service()
        files = self.client(service).file
        part, etags, _sent = files.upload_chunks(
            io.BytesIO(b"abcdefgh"), "c.bin"
        )
        rebuilt = FileUploadPart(part.get_attributes())
        with self.assertRaisesRegex(
            InvalidRequestError, "needs the FileUploadPart"
        ):
            files.upload_chunks(io.BytesIO(b"ijkl"), "c.bin", rebuilt, etags)
        self.assertEqual(sorted(service.stored), [1, 2])

    def test_a_remote_file_sends_the_offsets_of_the_whole_upload(self):
        service = self.service()
        with self.client(service).file.open("w.bin", "wb") as remote:
            remote.write(b"abcdef")
            remote.flush()
            remote.write(b"ghij")
        self.assertEqual(self.offsets(service), [(1, "0"), (2, "4"), (3, "8")])
        self.assertEqual(service.assembled(), b"abcdefghij")


def _sdk_name(path):
    """Whether path names one of the SDK's temporary entries."""
    if not isinstance(path, (str, bytes, os.PathLike)):
        return False
    name = os.path.basename(os.fsdecode(path))
    return name.startswith(".files_sdk-") or name.endswith(
        ".files_sdk-download"
    )


def _before(real, change):
    """real, running change() first, once, when change decides to."""

    def call(*args, **kwargs):
        change(*args)
        return real(*args, **kwargs)

    return call


@unittest.skipIf(sys.platform == "win32", "POSIX directory descriptors")
class TestAnchoredFilesystem(BoundaryTestCase):
    def test_entries_swapped_just_before_publication_never_publish_a_foreign_file(
        self,
    ):
        data = content(3000)
        service = DownloadService(self, data)
        target = self.scratch / "a.bin"
        target.write_bytes(b"previous")
        real_rename = os.rename
        swapped = []

        def swap(*_args):
            # What another user who can write the directory can do: move
            # the SDK's entries aside and put others of the same names in
            # their place, just as the finished file is renamed into place.
            if swapped:
                return
            for name in os.listdir(self.scratch):
                if not _sdk_name(name):
                    continue
                path, aside = self.scratch / name, self.scratch / (
                    "aside" + name
                )
                real_rename(path, aside)
                if aside.is_dir():
                    path.mkdir()
                    for inner in os.listdir(aside):
                        (path / inner).write_bytes(b"FOREIGN")
                else:
                    path.write_bytes(b"FOREIGN")
                swapped.append(name)

        with (
            mock.patch("os.rename", _before(os.rename, swap)),
            mock.patch("os.replace", _before(os.replace, swap)),
        ):
            self.client(service).file.download_file("a.bin", target)
        self.assertTrue(swapped)
        self.assertEqual(target.read_bytes(), data)
        # The entries put in the SDK's place are left as they were.
        for name in swapped:
            put = self.scratch / name
            self.assertTrue(
                all(
                    (put / inner).read_bytes() == b"FOREIGN"
                    for inner in os.listdir(put)
                )
            )

    def test_a_folder_swapped_for_a_link_before_the_stage_is_made_leaves_nothing_outside(
        self,
    ):
        service = TreeService(self, {"docs/sub/deep.txt": b"remote deep"})
        mirror, outside = self.scratch / "mirror", self.scratch / "outside"
        mirror.mkdir()
        outside.mkdir()
        seen_outside = []
        service.on_download = lambda _path: seen_outside.append(
            sorted(os.listdir(outside))
        )
        swapped = []

        def swap(path, *_args):
            if swapped or not _sdk_name(path):
                return
            os.replace(mirror / "sub", mirror / "sub-moved")
            (mirror / "sub").symlink_to(outside, target_is_directory=True)
            swapped.append(True)

        with (
            mock.patch("os.mkdir", _before(os.mkdir, swap)),
            mock.patch("os.open", _before(os.open, swap)),
        ):
            self.client(service).file.download_directory("docs", mirror)
        self.assertTrue(swapped)
        self.assertTrue(seen_outside)
        self.assertEqual([entries for entries in seen_outside if entries], [])
        self.assertEqual(os.listdir(outside), [])
        # The file went into the folder the job had opened, wherever it is now.
        self.assertEqual(
            (mirror / "sub-moved" / "deep.txt").read_bytes(), b"remote deep"
        )

    def test_the_stage_is_owner_only_from_the_moment_it_exists(self):
        service = DownloadService(self, content(2500))
        made, opened = [], []

        def recorder(calls):
            def record(path, *args):
                if _sdk_name(path):
                    calls.append((os.path.basename(os.fsdecode(path)), args))

            return record

        with (
            mock.patch("os.mkdir", _before(os.mkdir, recorder(made))),
            mock.patch("os.open", _before(os.open, recorder(opened))),
        ):
            self.client(service).file.download_file(
                "a.bin", self.scratch / "a.bin"
            )
        [(directory, (directory_mode,))] = made
        self.assertTrue(directory.startswith(".files_sdk-"))
        self.assertEqual(directory_mode, 0o700)
        [(_name, (flags, mode))] = [
            (name, args)
            for name, args in opened
            if name.endswith(".files_sdk-download")
        ]
        self.assertEqual(mode, 0o600)
        self.assertEqual(
            flags & (os.O_CREAT | os.O_EXCL), os.O_CREAT | os.O_EXCL
        )

    def test_a_shared_directory_keeps_its_permissions_and_group(self):
        shared = self.scratch / "shared"
        shared.mkdir()
        os.chmod(shared, 0o2775)
        before = os.stat(shared)
        umask = os.umask(0o002)
        try:
            self.client(DownloadService(self, b"shared")).file.download_file(
                "a.bin", shared / "a.bin"
            )
        finally:
            os.umask(umask)
        after = os.stat(shared)
        self.assertEqual(
            stat.S_IMODE(after.st_mode), stat.S_IMODE(before.st_mode)
        )
        published = os.stat(shared / "a.bin")
        self.assertEqual(
            (published.st_gid, stat.S_IMODE(published.st_mode)),
            (before.st_gid, 0o664),
        )
        self.assertEqual(sdk_entries(shared), [])

    def test_an_upload_walk_never_follows_a_folder_swapped_for_a_link(self):
        root, outside = self.scratch / "source", self.scratch / "outside"
        (root / "sub").mkdir(parents=True)
        (root / "sub" / "mine.txt").write_bytes(b"mine")
        outside.mkdir()
        (outside / "secret.txt").write_bytes(b"SECRET")
        service = UploadService(self, part_size=1000)
        swapped = []

        def swap(path, *_args):
            if (
                swapped
                or not isinstance(path, (str, os.PathLike))
                or os.path.basename(os.fspath(path)) != "sub"
            ):
                return
            os.replace(root / "sub", self.scratch / "sub-moved")
            (root / "sub").symlink_to(outside, target_is_directory=True)
            swapped.append(True)

        with (
            mock.patch("os.open", _before(os.open, swap)),
            mock.patch("os.scandir", _before(os.scandir, swap)),
        ):
            result = self.client(service).file.upload_directory(root, "up")
        self.assertTrue(swapped)
        self.assertEqual(service.completed_paths(), [])
        [failed] = result.failed
        self.assertEqual(
            (failed.kind, failed.remote_path), ("folder", "up/sub")
        )

    def test_a_file_swapped_for_a_link_after_it_was_found_is_not_uploaded(
        self,
    ):
        root, outside = self.scratch / "source", self.scratch / "outside"
        root.mkdir()
        outside.mkdir()
        (root / "a.txt").write_bytes(b"a")
        (root / "b.txt").write_bytes(b"b")
        (outside / "secret.txt").write_bytes(b"SECRET")
        service = UploadService(self, part_size=1000)

        def swap(_number):
            if not (root / "b.txt").is_symlink():
                (root / "b.txt").unlink()
                (root / "b.txt").symlink_to(outside / "secret.txt")

        service.on_put = swap
        result = self.client(service).file.upload_directory(
            root, "up", max_files=1
        )
        self.assertEqual(service.completed_paths(), ["up/a.txt"])
        [failed] = result.failed
        self.assertEqual(failed.remote_path, "up/b.txt")
        self.assertIn("replaced after it was found", str(failed.error))


class Trickle(io.RawIOBase):
    """A blocking stream that takes at most `most` bytes of each write."""

    def __init__(self, most, on_write=None):
        self.most = most
        self.data = bytearray()
        self.writes = 0
        self.on_write = on_write

    def writable(self):
        return True

    def write(self, data):
        self.writes += 1
        if self.on_write is not None:
            self.on_write(self)
        taken = bytes(memoryview(data)[: self.most])
        self.data += taken
        return len(taken)

    def tell(self):
        return len(self.data)


class TextTrickle(io.TextIOBase):
    """A text stream that takes at most `most` characters of each write."""

    def __init__(self, most):
        self.most = most
        self.text = ""

    def writable(self):
        return True

    def write(self, text):
        self.text += text[: self.most]
        return min(len(text), self.most)


class TestExactStreamWrites(BoundaryTestCase):
    def test_short_writes_deliver_every_byte_exactly_once_on_every_route(self):
        data = content(4500)
        for label in ("ranges", "whole", "file method", "api client"):
            with self.subTest(label):
                stream = Trickle(7)
                if label == "api client":
                    api = serve_loopback_api(self)
                    api.reply(200, data)
                    ApiClient().stream_download(api.url + "/storage/x", stream)
                else:
                    service = DownloadService(self, data)
                    if label == "whole":
                        service.identity = "absent"
                    client = self.client(service)
                    if label == "file method":
                        file = client.file.download_stream(
                            "a.bin", io.BytesIO()
                        )
                        file.download_content(stream)
                    else:
                        client.file.download_stream("a.bin", stream)
                self.assertEqual(bytes(stream.data), data)

    def test_short_text_writes_deliver_every_character_exactly_once(self):
        text = "é€ text\n" * 600
        service = DownloadService(self, text.encode("utf-8"))
        stream = TextTrickle(5)
        file = self.client(service).file.download_stream("t.txt", io.BytesIO())
        file.download_content(stream, is_string_io=True)
        self.assertEqual(stream.text, text)

    def test_a_stream_that_takes_nothing_or_would_block_is_refused(self):
        data = content(2500)

        class Would(io.RawIOBase):
            def writable(self):
                return True

            def write(self, _data):
                return None

        class Plain:
            def __init__(self):
                self.data = b""

            def write(self, data):
                self.data += bytes(data)

        for stream, message in (
            (Trickle(0), "took nothing"),
            (Would(), "would block"),
        ):
            with self.subTest(message):
                with self.assertRaisesRegex(InvalidParameterError, message):
                    self.client(
                        DownloadService(self, data)
                    ).file.download_stream("a.bin", stream)
        # A simple writer that returns nothing took everything, as before.
        plain = Plain()
        self.client(DownloadService(self, data)).file.download_stream(
            "a.bin", plain
        )
        self.assertEqual(plain.data, data)

    def test_cancelling_during_a_write_starts_no_further_write(self):
        service = DownloadService(self, content(4500))
        token = files_sdk.CancellationToken()
        stream = Trickle(100, on_write=lambda _stream: token.cancel())
        with self.assertRaises(OperationCancelledError):
            self.client(service).file.download_stream(
                "a.bin", stream, {"cancel_token": token}
            )
        self.assertEqual((stream.writes, len(stream.data)), (1, 100))

    def test_a_failure_after_part_of_a_write_is_counted_exactly_and_resumed_without_replay(
        self,
    ):
        data = content(4500)
        service = DownloadService(self, data)
        checkpoint = self.scratch / "d.checkpoint"
        mine = OSError("the caller's disk is full")

        def fail_second(stream):
            if stream.writes == 2:
                raise mine

        stream = Trickle(300, on_write=fail_second)
        with self.assertRaises(OSError) as caught:
            self.client(service).file.download_stream(
                "a.bin", stream, max_concurrency=1, checkpoint=checkpoint
            )
        self.assertIs(caught.exception, mine)
        self.assertEqual(bytes(stream.data), data[:300])
        stream.on_write = None
        stream.most = 1 << 20
        self.client(service).file.download_stream(
            "a.bin", stream, checkpoint=checkpoint
        )
        self.assertEqual(bytes(stream.data), data)


class TestSerialRenewal(BoundaryTestCase):
    def test_an_expired_grant_of_a_serial_upload_is_renewed_with_its_granted_part_size(
        self,
    ):
        for data in (b"abcdefgh", b"abcdefghij"):
            for route in ("stream", "chunks", "remote file"):
                with self.subTest(size=len(data), route=route):
                    service = UploadService(
                        self, part_size=4, grant={"parallel_parts": False}
                    )
                    service.expire_first()
                    files = self.client(service).file
                    if route == "stream":
                        files.upload_stream(io.BytesIO(data), "u.bin")
                        self.assertEqual(service.assembled(), data)
                    elif route == "chunks":
                        _part, etags, sent = files.upload_chunks(
                            io.BytesIO(data), "u.bin"
                        )
                        self.assertEqual(
                            (sent, len(etags)),
                            (len(data), len(service.stored)),
                        )
                    else:
                        with files.open("u.bin", "wb") as remote:
                            remote.write(data)
                        self.assertEqual(service.assembled(), data)
                    # Every part's first grant had expired; each was renewed once.
                    self.assertEqual(set(service.issued.values()), {2})
                    self.assertEqual(
                        b"".join(
                            service.part(n) for n in sorted(service.stored)
                        ),
                        data,
                    )


if __name__ == "__main__":
    unittest.main()

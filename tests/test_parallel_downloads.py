import errno
import io
import json
import os
import random
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock
from urllib.parse import urlsplit

import requests

import files_sdk
from files_sdk.error import (
    APIConnectionError,
    APIError,
    InvalidBodyError,
    InvalidParameterError,
    InvalidRequestError,
    OperationCancelledError,
)
from files_sdk import localfs
from files_sdk.adaptive import Controller
from files_sdk.download import _CHUNK
from files_sdk.lifetime import CancellationToken, Lifetime
from files_sdk.localfs import AccessNotKept
from files_sdk.upload import _admitted
from tests.download_fixtures import (
    S3_ORIGIN,
    DownloadService,
    sdk_entries,
    token_of,
)

RANGE = 1000


class DownloadTestCase(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)
        # Small ranges, so small files have several.
        patch = mock.patch("files_sdk.download.DEFAULT_RANGE_SIZE", RANGE)
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

    def bound(self, service, by, **settings):
        """A client of service, with settings, whose downloads are bound to a
        version by Files.com's download identity ("identity"), or, without
        one, from Amazon S3 by storage's own first answer ("storage")."""
        if by == "identity":
            return self.client(service, **settings)
        session = service.bound_by_storage()
        self.addCleanup(session.close)
        return self.client(service, http_session=session, **settings)

    def stages(self):
        return sdk_entries(self.scratch)

    def stage_files(self):
        return [
            name
            for name in self.stages()
            if name.endswith(".files_sdk-download")
        ]

    def existing(self, data=b"old content", name="out.bin"):
        path = self.scratch / name
        path.write_bytes(data)
        return path


def content(size, seed=1):
    return random.Random(seed).randbytes(size)


class TestRangedDownloads(DownloadTestCase):
    def test_ranges_finish_out_of_order_and_land_exactly(self):
        data = content(9500)
        service = DownloadService(self, data)
        # Earlier ranges take longer, so later ones finish first.
        service.delay = lambda start: 0.02 * (10 - start // RANGE)

        file = self.client(service).file.download_file(
            "dir/big.bin", self.scratch / "big.bin"
        )

        self.assertEqual((self.scratch / "big.bin").read_bytes(), data)
        self.assertEqual(file.path, "dir/big.bin")
        self.assertEqual(
            sorted(service.ranges(), key=lambda r: int(r[6:].split("-")[0])),
            [
                "bytes={}-{}".format(s, min(s + RANGE, 9500) - 1)
                for s in range(0, 9500, RANGE)
            ],
        )
        self.assertGreater(service.max_active, 1)
        self.assertEqual(
            {r["encoding"] for r in service.storage_requests()}, {"identity"}
        )
        self.assertEqual(self.stages(), [])

    def test_a_stream_receives_ranges_in_order(self):
        data = content(9500)
        service = DownloadService(self, data)
        service.delay = lambda start: 0.02 * (10 - start // RANGE)
        writes = []

        class Recording(io.BytesIO):
            def write(self, chunk):
                writes.append((self.tell(), type(chunk)))
                return super().write(chunk)

        output = Recording()
        output.write(b"kept")
        writes.clear()
        file = self.client(service).file.download_stream("big.bin", output)

        self.assertEqual(output.getvalue(), b"kept" + data)
        positions = [position for position, _type in writes]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual({kind for _position, kind in writes}, {bytes})
        self.assertGreater(service.max_active, 1)
        self.assertFalse(output.closed)
        self.assertEqual(file.path, "big.bin")

    def test_max_concurrency_one_fetches_one_range_at_a_time(self):
        data = content(5000)
        service = DownloadService(self, data)
        service.delay = lambda start: 0.01
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin", max_concurrency=1
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        self.assertEqual(service.max_active, 1)

    def test_the_storage_size_replaces_a_stale_reported_size(self):
        data = content(5500)
        for reported in (0, 100, 99999, None):
            with self.subTest(reported=reported):
                service = DownloadService(self, data, reported_size=reported)
                output = io.BytesIO()
                self.client(service).file.download_stream("a.bin", output)
                self.assertEqual(output.getvalue(), data)

    def test_every_range_carries_the_versions_if_match_and_is_checked_against_it(
        self,
    ):
        data = content(5000)
        service = DownloadService(self, data)
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        self.assertEqual(
            {r["if_match"] for r in service.storage_requests()}, {service.etag}
        )
        [negotiation] = service.negotiations
        # As every boolean in a query goes (Files.com reads True as true).
        self.assertEqual(negotiation.get("with_download_identity"), "True")
        self.assertNotIn("expected_download_identity", negotiation)

    def test_storage_that_ignores_ranges_fails_an_identified_download(self):
        # A whole file for a range is never taken for the range.
        service = DownloadService(self, content(5000))
        service.ignore_ranges = True
        path = self.existing()
        with self.assertRaisesRegex(
            APIConnectionError, "bytes .* was answered with HTTP 200"
        ):
            self.client(service).file.download_file("a.bin", path)
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])
        # Bound by storage's own first answer, a later range answered with the
        # whole file of that version (its ETag) is not taken for the range
        # either: the version is read in one response, with If-Match, what the
        # ranges wrote discarded. A stream that has taken bytes cannot take the
        # file again, so that download fails, holding only its first range.
        data = content(5000)
        with self.subTest("bound by storage, to a path"):
            service = DownloadService(self, data)
            service.ignore_ranges_after = 1
            path = self.existing()
            self.bound(service, "storage").file.download_file("a.bin", path)
            self.assertEqual(path.read_bytes(), data)
            [first, *later] = service.storage_requests()
            self.assertEqual(
                ("bytes=0-{}".format(RANGE - 1), None),
                (first["range"], first["if_match"]),
            )
            self.assertEqual(
                [None],
                [
                    request["range"]
                    for request in later
                    if request["range"] is None
                ],
            )
            self.assertEqual(
                {service.etag}, {request["if_match"] for request in later}
            )
            self.assertEqual(self.stages(), [])
        with self.subTest(
            "bound by storage, to a stream that has taken bytes"
        ):
            service = DownloadService(self, data)
            service.ignore_ranges_after = 1
            output = io.BytesIO()
            with self.assertRaisesRegex(
                APIConnectionError,
                "after part of the file had reached the stream",
            ):
                self.bound(service, "storage").file.download_stream(
                    "a.bin", output, max_concurrency=1
                )
            self.assertEqual(output.getvalue(), data[:RANGE])
            self.assertNotIn(None, service.ranges())

    def test_an_encoded_range_is_refused_and_an_encoded_whole_answer_is_decoded(
        self,
    ):
        data = b"compressible " * 800
        with self.subTest("encoded range"):
            service = DownloadService(self, data)
            service.gzip = "all"
            output = io.BytesIO()
            with self.assertRaisesRegex(
                APIConnectionError, "a range came encoded"
            ):
                self.client(service).file.download_stream("a.txt", output)
            self.assertEqual(output.getvalue(), b"")
        with self.subTest("encoded whole answer, without a download identity"):
            service = DownloadService(self, data)
            service.gzip = "all"
            service.identity = "absent"
            self.client(service).file.download_file(
                "a.txt", self.scratch / "a.txt"
            )
            self.assertEqual((self.scratch / "a.txt").read_bytes(), data)
            self.assertEqual(service.ranges(), [None])

    def test_an_empty_version_is_one_request_for_the_whole_of_it(self):
        service = DownloadService(self, b"")
        path = self.existing(b"previous")
        self.client(service).file.download_file("empty.bin", path)
        self.assertEqual(path.read_bytes(), b"")
        self.assertEqual(service.ranges(), [None])
        self.assertEqual(
            service.storage_requests()[0]["if_match"], service.etag
        )
        output = io.BytesIO()
        self.client(service).file.download_stream("empty.bin", output)
        self.assertEqual(output.getvalue(), b"")

    def test_a_small_file_is_one_range(self):
        data = content(300)
        service = DownloadService(self, data)
        self.client(service).file.download_file(
            "s.bin", self.scratch / "s.bin"
        )
        self.assertEqual((self.scratch / "s.bin").read_bytes(), data)
        self.assertEqual(service.ranges(), ["bytes=0-299"])
        # Without an identity, from S3, the first range is planned before the
        # file's size is known: the one answer is the whole small file. With
        # a strong ETag it binds the download; without one it is still the
        # file, unbound. Either way the controller learns the bytes that
        # arrived, not the range planned.
        controllers = []
        real = files_sdk.download.Controller

        def made(*args, **kwargs):
            controllers.append(real(*args, **kwargs))
            return controllers[-1]

        for etag_style in ("strong", "weak"):
            with self.subTest(etag=etag_style):
                service = DownloadService(self, data)
                service.etag_style = etag_style
                client = self.bound(service, "storage")
                path = self.scratch / "{}.bin".format(etag_style)
                reports = []
                with mock.patch.object(files_sdk.download, "Controller", made):
                    client.file.download_file(
                        "s.bin", path, progress=reports.append
                    )
                self.assertEqual(path.read_bytes(), data)
                self.assertEqual(
                    ["bytes=0-{}".format(RANGE - 1)], service.ranges()
                )
                self.assertEqual(
                    [None],
                    [
                        request["if_match"]
                        for request in service.storage_requests()
                    ],
                )
                self.assertEqual(len(data), controllers[-1].bytes_total)
                self.assertEqual(
                    etag_style == "strong", reports[-1].pinned_version
                )
                self.assertEqual(self.stages(), [])
        # Unbound, the first answer, a file within one range, is cut short
        # after the SDK has written part of it; the retry's answer is a
        # shorter file, whole. The file is exactly that shorter one, with
        # nothing of the first answer after it.
        with self.subTest("a shorter file in the answer to the retry"):
            first, second = content(4 * 1024 * 1024, seed=2), content(
                _CHUNK, seed=3
            )
            service = DownloadService(self, first)
            service.etag_style = "weak"
            service.short_once = {0}
            service.change_after = (1, second)
            path = self.scratch / "shorter.bin"
            reports = []
            limiter = files_sdk.TransferLimiter()
            client = self.bound(service, "storage", transfer_limiter=limiter)
            with (
                mock.patch.object(files_sdk.download, "Controller", made),
                mock.patch(
                    "files_sdk.download.DEFAULT_RANGE_SIZE", len(first)
                ),
            ):
                client.file.download_file(
                    "s.bin", path, progress=reports.append
                )
            self.assertEqual(second, path.read_bytes())
            self.assertEqual(
                ["bytes=0-{}".format(len(first) - 1)] * 2, service.ranges()
            )
            last = reports[-1]
            self.assertEqual(
                (len(second), len(second), False),
                (last.total_bytes, last.bytes_committed, last.pinned_version),
            )
            # Only the answer taken counts as accepted bytes; nothing stays held.
            self.assertEqual(len(second), controllers[-1].bytes_total)
            self.assertEqual(
                (0, 0), (limiter.parts_in_use, limiter.bytes_in_use)
            )
            self.assertEqual(self.stages(), [])


class TestDownloadIdentity(DownloadTestCase):
    """A download is bound to one version of the file by its download
    identity, or read in one response without one."""

    def test_without_an_identity_a_changing_file_is_never_assembled_from_two_versions(
        self,
    ):
        # The file changes after storage's first answer. Storage shows no
        # ETag, or the same weak one for both versions, so nothing tells
        # the versions apart: the file is read in one response.
        old, new = content(16000, seed=1), content(16000, seed=2)
        for switch, etag_style in (
            ("absent", None),
            ("absent", "weak"),
            ("unavailable", None),
            ("unavailable", "weak"),
        ):
            with self.subTest(identity=switch, etag=etag_style):
                service = DownloadService(self, old)
                service.identity = switch
                service.etag_style = etag_style
                service.change_after = (1, new)
                path = self.existing()
                self.client(service).file.download_file("a.bin", path)
                self.assertEqual(path.read_bytes(), old)
                self.assertEqual(service.ranges(), [None])
                self.assertEqual(
                    {r["if_match"] for r in service.storage_requests()}, {None}
                )
                output = io.BytesIO()
                self.client(service).file.download_stream("a.bin", output)
                self.assertEqual(output.getvalue(), new)
                if switch == "unavailable":
                    # Asked for an identity, then for the file without one.
                    self.assertEqual(
                        [
                            q.get("with_download_identity")
                            for q in service.negotiations
                        ],
                        ["True", None, "True", None],
                    )

    def test_without_an_identity_a_response_cut_short_starts_again_only_where_nothing_was_exposed(
        self,
    ):
        # Long enough that the stream takes a chunk before the cut.
        data = content(3 * _CHUNK)
        service = DownloadService(self, data)
        service.identity = "absent"
        service.whole_short_once = 1
        path = self.existing()
        reports = []
        self.client(service).file.download_file(
            "a.bin", path, progress=reports.append
        )
        self.assertEqual(path.read_bytes(), data)
        self.assertEqual(service.ranges(), [None, None])
        # The second read counts from zero again; what the first read took
        # stays received, and the rate never goes negative.
        last = reports[-1]
        self.assertEqual(
            (last.total_bytes, last.bytes_committed, last.ranges_committed),
            (len(data), len(data), 1),
        )
        self.assertGreater(last.bytes_received, len(data))
        self.assertTrue(
            all(report.bytes_per_second >= 0 for report in reports)
        )
        # A stream that took the first half cannot take the file again.
        service.whole_short_once = 1
        service.requests.clear()
        output = io.BytesIO()
        with self.assertRaises(APIConnectionError):
            self.client(service).file.download_stream("a.bin", output)
        self.assertTrue(output.getvalue())
        self.assertEqual(output.getvalue(), data[: len(output.getvalue())])
        self.assertEqual(service.ranges(), [None])

    def test_without_an_identity_progress_and_size_arrive_while_the_response_is_read(
        self,
    ):
        # Storage holds back the last 64 KiB of its answer until the progress
        # callback is called, so what the callback saw came before the whole
        # file arrived.
        data = content(3 * _CHUNK)
        for route, encoded in (
            ("path", False),
            ("stream", False),
            ("path", True),
        ):
            with self.subTest(route=route, encoded=encoded):
                service = DownloadService(self, data)
                service.identity = "absent"
                if encoded:
                    service.gzip = "all"
                release = threading.Event()
                self.addCleanup(release.set)
                service.hold_whole = release
                reports, early = [], []

                def report(progress):
                    reports.append(progress)
                    if not release.is_set():
                        early.append(progress)
                        release.set()

                client = self.client(service)
                if route == "path":
                    client.file.download_file(
                        "a.bin", self.scratch / "a.bin", progress=report
                    )
                    received = (self.scratch / "a.bin").read_bytes()
                else:
                    output = io.BytesIO()
                    client.file.download_stream(
                        "a.bin", output, progress=report
                    )
                    received = output.getvalue()
                self.assertEqual(received, data)
                self.assertEqual(service.ranges(), [None])
                # The callback, not the time limit, let storage go on.
                self.assertFalse(service.hold_timed_out)
                [first] = early
                # An encoded answer's Content-Length is not the file's size.
                self.assertEqual(
                    first.total_bytes, None if encoded else len(data)
                )
                self.assertFalse(first.pinned_version)
                self.assertGreater(first.bytes_committed, 0)
                self.assertLess(first.bytes_committed, len(data))
                self.assertLessEqual(
                    first.bytes_committed, first.bytes_received
                )
                last = reports[-1]
                self.assertEqual(
                    (
                        last.total_bytes,
                        last.bytes_committed,
                        last.ranges_committed,
                    ),
                    (len(data), len(data), 1),
                )
                committed = [report.bytes_committed for report in reports]
                self.assertEqual(committed, sorted(committed))

    def test_a_whole_answer_that_runs_past_its_length_reaches_nothing_beyond_it(
        self,
    ):
        data = content(3000)
        for destination in ("path", "stream"):
            with self.subTest(destination):
                service = DownloadService(self, data)
                service.identity = "absent"
                service.whole_overrun_once = 64
                if destination == "path":
                    self.client(service).file.download_file(
                        "a.bin", self.scratch / "a.bin"
                    )
                    received = (self.scratch / "a.bin").read_bytes()
                else:
                    output = io.BytesIO()
                    self.client(service).file.download_stream("a.bin", output)
                    received = output.getvalue()
                # Refused before any of it was written, so read again.
                self.assertEqual(received, data)
                self.assertEqual(service.ranges(), [None, None])

    def test_an_invalid_identity_fails_before_storage_is_asked_for_anything(
        self,
    ):
        def replacing(**changes):
            return lambda identity, _renewal: {**identity, **changes}

        cases = {
            "version 2": replacing(version=2),
            "version true": replacing(version=True),
            "no token": replacing(token=None),
            "token with a space": replacing(token="a b"),
            "token too long": replacing(token="t" * 4097),
            "negative size": replacing(size=-1),
            "size as text": replacing(size="5000"),
            "size true": replacing(size=True),
            "headers not an object": replacing(required_headers=["If-Match"]),
            "another header": replacing(
                required_headers={"If-None-Match": '"x"'}
            ),
            "two headers": replacing(
                required_headers={"If-Match": '"x"', "Range": "bytes=0-1"}
            ),
            "weak If-Match": replacing(required_headers={"If-Match": 'W/"x"'}),
            "wildcard If-Match": replacing(required_headers={"If-Match": "*"}),
            "unquoted If-Match": replacing(required_headers={"If-Match": "x"}),
            "not an object": lambda identity, _renewal: "v1",
        }
        for label, tamper in cases.items():
            with self.subTest(label):
                service = DownloadService(self, content(5000))
                service.tamper = tamper
                path = self.existing()
                with self.assertRaisesRegex(
                    APIConnectionError, "invalid download identity"
                ):
                    self.client(service).file.download_file("a.bin", path)
                self.assertEqual(path.read_bytes(), b"old content")
                self.assertEqual(service.storage_requests(), [])
                self.assertEqual(self.stages(), [])

    def test_a_token_of_4096_characters_is_accepted(self):
        data = content(2500)
        service = DownloadService(self, data)
        service.identity = "proxy"
        service.tamper = lambda identity, _renewal: {
            **identity,
            "token": "t" * 4096,
        }
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)

    def test_a_renewal_that_gives_another_version_restarts_a_path_and_fails_an_exposed_stream(
        self,
    ):
        data = content(9000)
        for changed in ("token", "size"):
            with self.subTest(changed):
                service = DownloadService(self, data)

                def tamper(identity, renewal, changed=changed):
                    if not renewal:
                        return identity
                    return (
                        {**identity, "token": "other"}
                        if changed == "token"
                        else {**identity, "size": identity["size"] + 1}
                    )

                service.tamper = tamper
                service.expire_first_url = 2
                service.delay = lambda start: 0.01
                path = self.existing()
                self.client(service).file.download_file(
                    "a.bin", path, max_concurrency=1
                )
                self.assertEqual(path.read_bytes(), data)
                # Renewed once, refused, then negotiated afresh.
                self.assertEqual(
                    [
                        bool(q.get("expected_download_identity"))
                        for q in service.negotiations
                    ],
                    [False, True, False],
                )
                service.negotiations.clear()
                service.expire_first_url = None
                service.served = 0
                service.issued = 0
                service.expire_first_url = 2
                output = io.BytesIO()
                with self.assertRaisesRegex(
                    InvalidRequestError,
                    "changed while it was being downloaded",
                ):
                    self.client(service).file.download_stream(
                        "a.bin", output, max_concurrency=1
                    )
                self.assertEqual(
                    output.getvalue(), data[: len(output.getvalue())]
                )

    def test_a_weak_etag_where_if_match_was_sent_is_refused(self):
        service = DownloadService(self, content(5000))
        service.etag_style = "weak"
        path = self.existing()
        with self.assertRaisesRegex(
            APIConnectionError, "weak or malformed ETag"
        ):
            self.client(service).file.download_file("a.bin", path)
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])

    def test_a_response_without_an_etag_from_the_url_s_origin_is_taken(self):
        # The contract compares an ETag that comes back; the If-Match went
        # to the URL's origin, which enforces it.
        data = content(5000)
        service = DownloadService(self, data)
        service.etag_style = None
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        self.assertEqual(
            {r["if_match"] for r in service.storage_requests()}, {service.etag}
        )

    def test_storage_that_ignores_the_if_match_and_shows_another_tag_is_a_changed_source(
        self,
    ):
        old, new = content(5000, seed=1), content(5000, seed=2)
        service = DownloadService(self, old)
        service.ignore_if_match = True
        service.change_after = (2, new)
        path = self.existing()
        self.client(service).file.download_file(
            "a.bin", path, max_concurrency=1
        )
        self.assertEqual(path.read_bytes(), new)
        service = DownloadService(self, old)
        service.ignore_if_match = True
        service.change_after = (2, new)
        output = io.BytesIO()
        with self.assertRaisesRegex(
            InvalidRequestError, "changed while it was being downloaded"
        ):
            self.client(service).file.download_stream(
                "a.bin", output, max_concurrency=1
            )
        self.assertEqual(output.getvalue(), old[:2000])

    def test_a_redirect_to_another_origin_is_refused_before_it_is_followed(
        self,
    ):
        # Another origin can show the same ETag text for other content: its
        # tag is no proof of the version, and the If-Match cannot go there.
        for identity in ("if-match", "proxy"):
            with self.subTest(identity=identity):
                service = DownloadService(self, b"AAAA" * 750)
                elsewhere = DownloadService(self, b"BBBB" * 750)
                for origin in (service, elsewhere):
                    origin.identity = identity
                    origin.etag_text = '"revision-one"'
                service.redirect_to = elsewhere.url
                path = self.existing()
                with self.assertRaisesRegex(
                    APIConnectionError, "another origin than its URL's"
                ):
                    self.client(service).file.download_file("a.bin", path)
                output = io.BytesIO()
                with self.assertRaisesRegex(
                    APIConnectionError, "another origin than its URL's"
                ):
                    self.client(service).file.download_stream("a.bin", output)
                # Nothing, and no header, was sent there.
                self.assertEqual(elsewhere.storage_requests(), [])
                self.assertEqual(
                    (path.read_bytes(), output.getvalue(), self.stages()),
                    (b"old content", b"", []),
                )

    def test_a_redirect_within_the_url_s_origin_keeps_the_if_match(self):
        data = content(3000)
        service = DownloadService(self, data)
        service.redirect_to = service.url
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        requests_made = service.storage_requests()
        self.assertEqual(len(requests_made), 6)  # Each range redirected once.
        self.assertEqual(
            {r["if_match"] for r in requests_made}, {service.etag}
        )

    def test_a_download_without_an_identity_still_follows_a_redirect_elsewhere(
        self,
    ):
        data = content(3000)
        service = DownloadService(self, data)
        elsewhere = DownloadService(self, data)
        service.identity = elsewhere.identity = "absent"
        service.redirect_to = elsewhere.url
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        [followed] = elsewhere.storage_requests()
        self.assertEqual(
            (followed["if_match"], followed["authorization"]), (None, None)
        )

    def test_an_identity_without_headers_is_enforced_by_its_url(self):
        old, new = content(5000, seed=1), content(5000, seed=2)
        service = DownloadService(self, old)
        service.identity = "proxy"
        service.change_after = (2, new)
        path = self.existing()
        self.client(service).file.download_file("a.bin", path)
        self.assertEqual(path.read_bytes(), new)
        self.assertEqual(
            {r["if_match"] for r in service.storage_requests()}, {None}
        )

    def test_a_range_of_a_file_of_another_size_is_a_changed_source(self):
        service = DownloadService(self, content(5000))
        service.tamper = lambda identity, _renewal: {**identity, "size": 6000}
        path = self.existing()
        with self.assertRaisesRegex(
            InvalidRequestError, "changed while it was being downloaded"
        ):
            self.client(service).file.download_file("a.bin", path)
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])


class TestDownloadFailures(DownloadTestCase):
    def test_the_web_app_answering_fails_before_anything_is_written(self):
        service = DownloadService(self, content(5000))
        service.frontend = True
        path = self.existing()
        with self.assertRaisesRegex(APIConnectionError, "web app"):
            self.client(service).file.download_file("a.bin", path)
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])
        first = service.ranges()
        output = io.BytesIO()
        with self.assertRaisesRegex(APIConnectionError, "web app"):
            self.client(service).file.download_stream("a.bin", output)
        self.assertEqual(output.getvalue(), b"")
        # Not retried: another attempt reaches the same page.
        for ranges in (first, service.ranges()[len(first) :]):
            self.assertTrue(ranges)
            self.assertEqual(len(ranges), len(set(ranges)))

    def test_a_range_cut_short_is_fetched_again(self):
        data = content(5000)
        service = DownloadService(self, data)
        service.short_once = {2000}
        for destination in ("path", "stream"):
            with self.subTest(destination):
                service.short_once = {2000}
                service.requests.clear()
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

    def test_a_failed_range_is_retried(self):
        data = content(5000)
        service = DownloadService(self, data)
        service.fail(3000, status=503, times=2)
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        self.assertEqual(service.ranges().count("bytes=3000-3999"), 3)

    def test_a_range_that_fails_for_good_leaves_the_destination_as_it_was(
        self,
    ):
        service = DownloadService(self, content(5000))
        service.fail(3000, status=500, times=99)
        path = self.existing()
        with self.assertRaises(APIError) as caught:
            self.client(service, max_network_retries=1).file.download_file(
                "a.bin", path
            )
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])
        # Named once, however often the range was tried.
        self.assertEqual(
            str(caught.exception),
            "HTTP 500 Transfer request failed for the download of a.bin",
        )

    def test_a_range_that_runs_long_never_writes_past_its_own_bytes(self):
        # The second range is written first; then the first runs 64 bytes
        # long, in a well-framed chunked body.
        data = content(2000)
        service = DownloadService(self, data)
        second_written = threading.Event()
        service.delay = lambda start: (
            (second_written.wait(5), 0)[1] if start == 0 else 0
        )
        service.overrun_once = {0: 64}

        def progress(report):
            if report.bytes_committed >= RANGE:
                second_written.set()

        path = self.scratch / "a.bin"
        self.client(service).file.download_file(
            "a.bin", path, max_concurrency=2, progress=progress
        )
        self.assertEqual(path.read_bytes(), data)
        self.assertEqual(service.ranges().count("bytes=0-999"), 2)

    def test_correctly_chunked_ranges_are_taken(self):
        data = content(5000)
        for destination in ("path", "stream"):
            with self.subTest(destination):
                service = DownloadService(self, data)
                service.chunked = True
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
                self.assertEqual(len(service.ranges()), 5)

    def test_a_range_labelled_as_other_bytes_is_refused(self):
        service = DownloadService(self, content(5000))
        service.wrong_range_for = {3000}
        path = self.existing()
        with self.assertRaisesRegex(APIConnectionError, "other bytes"):
            self.client(service).file.download_file("a.bin", path)
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])

    def test_a_file_that_changes_restarts_a_path_download_once(self):
        # Bound by its download identity, or, without one, by storage's own
        # first answer, whose ETag the later ranges' If-Match must match.
        old, new = content(5000, seed=1), content(5000, seed=2)
        for by in ("identity", "storage"):
            for replacement in (new, new[:4200]):
                with self.subTest(by=by, size=len(replacement)):
                    service = DownloadService(self, old)
                    service.change_after = (2, replacement)
                    path = self.existing()
                    self.bound(service, by).file.download_file("a.bin", path)
                    self.assertEqual(path.read_bytes(), replacement)
                    self.assertEqual(self.stages(), [])
                    if by == "storage":
                        # Never sent to Files.com as if it were an identity.
                        self.assertTrue(
                            all(
                                "expected_download_identity" not in query
                                for query in service.negotiations
                            )
                        )

    def test_a_file_that_keeps_changing_is_not_published(self):
        service = DownloadService(self, content(5000))
        changes = iter(range(2, 1000))

        def change(_range):
            service.content = content(5000, seed=next(changes))

        service.on_request = change
        path = self.existing()
        with self.assertRaisesRegex(
            InvalidRequestError, "changed while it was being downloaded"
        ):
            self.client(service).file.download_file("a.bin", path)
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])

    def test_a_stream_download_of_a_file_that_changes_fails(self):
        old = content(5000, seed=1)
        for by in ("identity", "storage"):
            with self.subTest(by=by):
                service = DownloadService(self, old)
                service.change_after = (2, content(5000, seed=2))
                output = io.BytesIO()
                # One range at a time, so the stream has taken two when it changes.
                with self.assertRaisesRegex(
                    InvalidRequestError,
                    "changed while it was being downloaded",
                ):
                    self.bound(service, by).file.download_stream(
                        "a.bin", output, max_concurrency=1
                    )
                # What arrived is the old version's first ranges, never a mix.
                self.assertEqual(output.getvalue(), old[:2000])

    def test_an_expired_url_is_renewed_once_for_every_range(self):
        data = content(9000)
        service = DownloadService(self, data)
        # The probe succeeds, then every range meets the expired URL.
        service.expire_first_url = 1
        service.delay = lambda start: 0.02
        self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        self.assertEqual((self.scratch / "a.bin").read_bytes(), data)
        self.assertEqual(service.issued, 2)

    def test_a_url_that_stays_refused_fails_after_two_renewals_without_the_signature(
        self,
    ):
        service = DownloadService(self, content(5000))
        service.refuse_all = True
        path = self.existing()
        with self.assertRaises(APIError) as caught:
            self.client(service).file.download_file("a.bin", path)
        self.assertEqual(caught.exception.http_status, 403)
        self.assertEqual(service.issued, 3)
        # The last refusal, naming the file once; not the signed URL.
        self.assertEqual(
            str(caught.exception),
            "HTTP 403 Transfer request failed for the download of a.bin",
        )
        self.assertNotIn("secret", str(caught.exception))
        self.assertEqual(path.read_bytes(), b"old content")

    def expiry_cases(self):
        """(label, identity) for a download read in ranges and one read whole."""
        return (("ranges", "if-match"), ("whole", "unavailable"))

    def test_a_url_expired_by_its_own_signature_is_renewed_before_it_is_sent_again(
        self,
    ):
        data = content(3000)
        for label, identity in self.expiry_cases():
            for form in ("aws", "files", "google", "azure"):
                with self.subTest(label, form=form):
                    service = DownloadService(self, data)
                    service.identity = identity
                    service.signed = form
                    service.first_answer = (503, b"<html>busy</html>")
                    output = io.BytesIO()

                    self.client(service).file.download_stream(
                        "a.bin", output, max_concurrency=1
                    )

                    self.assertEqual(output.getvalue(), data)
                    # Tried once as given, then renewed instead of being sent again.
                    issues = [
                        request["issue"]
                        for request in service.storage_requests()
                    ]
                    self.assertEqual(
                        (issues[0], set(issues[1:])), ("1", {"2"})
                    )
                    self.assertEqual(service.issued, 2)
                    # Sent exactly as Files.com gave it, credentials only to Files.com.
                    self.assertEqual(
                        service.storage_requests()[-1]["query"],
                        urlsplit(service.uris[-1]).query,
                    )
                    self.assertEqual(
                        {None},
                        {
                            request["authorization"]
                            for request in service.storage_requests()
                        },
                    )
                    negotiations = [
                        request
                        for request in service.requests
                        if request["path"].startswith("/files/")
                    ]
                    self.assertEqual(
                        {"key"},
                        {request["authorization"] for request in negotiations},
                    )

    def test_a_url_storage_refuses_as_expired_is_renewed_and_other_refusals_are_raised(
        self,
    ):
        data = content(3000)
        expired = b"<Error><Code>ExpiredToken</Code><Message>The provided token has expired.</Message></Error>"
        denied = b"<Error><Code>AccessDenied</Code><Message>Access Denied</Message></Error>"
        for label, identity in self.expiry_cases():
            with self.subTest(label, answer="expired"):
                service = DownloadService(self, data)
                service.identity = identity
                service.first_answer = (400, expired)
                output = io.BytesIO()
                self.client(service).file.download_stream(
                    "a.bin", output, max_concurrency=1
                )
                self.assertEqual(output.getvalue(), data)
                self.assertEqual(service.issued, 2)
            with self.subTest(label, answer="denied"):
                service = DownloadService(self, data)
                service.identity = identity
                service.first_answer = (403, denied)
                with self.assertRaises(APIError) as caught:
                    self.client(service).file.download_stream(
                        "a.bin", io.BytesIO(), max_concurrency=1
                    )
                self.assertEqual(caught.exception.http_status, 403)
                self.assertEqual(service.issued, 1)
                self.assertEqual(
                    str(caught.exception),
                    "HTTP 403 Transfer request failed for the download of a.bin",
                )
                self.assertNotIn("AccessDenied", str(caught.exception))
            with self.subTest(label, answer="structured"):
                # A JSON refusal keeps the SDK error class its type names,
                # and what storage said stays in the error's body only.
                refusal = {
                    "type": "bad-request/invalid-body",
                    "error": "storage says no",
                    "http-code": 422,
                }
                service = DownloadService(self, data)
                service.identity = identity
                service.first_answer = (422, json.dumps(refusal).encode())
                with self.assertRaises(InvalidBodyError) as caught:
                    self.client(service).file.download_stream(
                        "a.bin", io.BytesIO(), max_concurrency=1
                    )
                self.assertEqual(caught.exception.http_status, 422)
                self.assertEqual(
                    caught.exception.json_body["type"],
                    "bad-request/invalid-body",
                )
                self.assertEqual(
                    str(caught.exception),
                    "HTTP 422 Transfer request failed for the download of a.bin",
                )

    def test_invalid_settings_are_refused_before_any_request_or_stage(self):
        service = DownloadService(self, content(100))
        client = self.client(service)
        for settings in (
            {"max_concurrency": 0},
            {"max_concurrency": 1025},
            {"progress": "no"},
            {"tuning": "static"},
            # Settings only an upload uses.
            {
                "tuning": files_sdk.UploadTuning(
                    startup=files_sdk.UploadStartup.AGGRESSIVE
                )
            },
            {"tuning": files_sdk.UploadTuning(adaptive=False, ready_parts=2)},
        ):
            with self.subTest(settings):
                with self.assertRaises(InvalidParameterError):
                    client.file.download_file(
                        "a.bin", self.scratch / "a.bin", **settings
                    )
                with self.assertRaises(InvalidParameterError):
                    client.file.download_stream(
                        "a.bin", io.BytesIO(), **settings
                    )
        with self.assertRaises(InvalidParameterError):
            client.file.download_stream("a.bin", object())
        self.assertEqual(service.requests, [])
        self.assertEqual(os.listdir(self.scratch), [])


@unittest.skipIf(sys.platform == "win32", "POSIX permissions and links")
class TestDownloadedFiles(DownloadTestCase):
    def test_an_existing_file_keeps_its_permissions_without_special_bits(self):
        service = DownloadService(self, content(2500))
        for before, after in (
            (0o640, 0o640),
            (0o4755, 0o755),
            (0o600, 0o600),
            (0o200, 0o200),
        ):
            with self.subTest(mode=oct(before)):
                path = self.existing()
                os.chmod(path, before)
                self.client(service).file.download_file("a.bin", path)
                self.assertEqual(stat.S_IMODE(os.stat(path).st_mode), after)

    def test_a_new_file_gets_the_permissions_a_new_file_would(self):
        service = DownloadService(self, content(2500))
        umask = os.umask(0o027)
        try:
            self.client(service).file.download_file(
                "a.bin", self.scratch / "new.bin"
            )
        finally:
            os.umask(umask)
        self.assertEqual(
            stat.S_IMODE(os.stat(self.scratch / "new.bin").st_mode), 0o640
        )

    def other_group(self):
        """A group of this process other than the one a new file here
        gets, so a file can be given it."""
        probe = self.existing(name="probe")
        default = os.stat(probe).st_gid
        probe.unlink()
        other = next(
            (group for group in os.getgroups() if group != default), None
        )
        if other is None:
            self.skipTest("the process is in only one group")
        return other

    def acl_of(self, path):
        """The access control entries of path, as the system lists them."""
        if sys.platform == "darwin":
            lines = subprocess.run(
                ["/bin/ls", "-lde", path],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
            return lines.splitlines()[1:]
        lines = subprocess.run(
            ["getfacl", "-c", path], capture_output=True, text=True, check=True
        ).stdout
        return [line for line in lines.splitlines() if line]

    def test_a_replaced_file_keeps_its_group(self):
        service = DownloadService(self, content(2500))
        group = self.other_group()
        path = self.existing()
        os.chown(path, -1, group)
        os.chmod(path, 0o640)

        self.client(service).file.download_file("a.bin", path)

        self.assertEqual(path.read_bytes(), service.content)
        self.assertEqual(
            (os.stat(path).st_gid, stat.S_IMODE(os.stat(path).st_mode)),
            (group, 0o640),
        )

    @unittest.skipUnless(
        sys.platform == "darwin" or shutil.which("setfacl"),
        "no access control lists to set",
    )
    def test_a_replaced_file_keeps_its_access_control_list(self):
        service = DownloadService(self, content(2500))
        path = self.existing()
        if sys.platform == "darwin":
            subprocess.run(
                ["/bin/chmod", "+a", "group:everyone allow read,write", path],
                check=True,
            )
        else:
            subprocess.run(["setfacl", "-m", "u:nobody:rw", path], check=True)
        before = self.acl_of(path)
        self.assertTrue(before)

        self.client(service).file.download_file("a.bin", path)

        self.assertEqual(path.read_bytes(), service.content)
        self.assertEqual(self.acl_of(path), before)

    def folder_that_moves(self, service, name):
        """A file of old content in a new folder, which service renames (to
        the path returned second) once the download is under way, while the
        SDK holds the folder open."""
        folder = self.scratch / name
        folder.mkdir()
        moved = self.scratch / (name + "-moved")
        path = folder / "out.bin"
        path.write_bytes(b"old content")
        lock = threading.Lock()

        def move(_range):
            with lock:
                if folder.exists():
                    folder.rename(moved)

        service.on_request = move
        return path, moved / "out.bin"

    @unittest.skipUnless(
        sys.platform == "darwin", "macOS access control lists"
    )
    def test_a_replaced_file_keeps_a_denying_access_control_list_after_its_folder_moves(
        self,
    ):
        service = DownloadService(self, content(2500))
        path, replaced = self.folder_that_moves(service, "folder")
        os.chmod(path, 0o604)
        subprocess.run(
            ["/bin/chmod", "+a", "group:everyone deny read", path], check=True
        )
        before = self.acl_of(path)

        self.client(service).file.download_file("a.bin", path)

        self.assertEqual(self.acl_of(replaced), before)
        with self.assertRaises(PermissionError):
            replaced.read_bytes()
        subprocess.run(["/bin/chmod", "-N", replaced], check=True)
        self.assertEqual(
            (replaced.read_bytes(), stat.S_IMODE(os.stat(replaced).st_mode)),
            (service.content, 0o604),
        )
        self.assertEqual(sdk_entries(replaced.parent), [])

    def test_a_linux_list_read_by_path_is_not_trusted_once_the_folder_moved(
        self,
    ):
        # Without /proc the list is read by path, which no longer leads to
        # the file: its answer, a list or none, is not taken for the file's.
        # /proc is made to look missing, as it is where Linux has none.
        linux = mock.patch.object(localfs, "sys", mock.Mock(platform="linux"))
        isdir = os.path.isdir
        no_proc = mock.patch(
            "os.path.isdir",
            lambda name: name != "/proc/self/fd" and isdir(name),
        )
        for failure in (None, errno.ENODATA):
            with self.subTest(failure=failure):
                service = DownloadService(self, content(2500))
                path, replaced = self.folder_that_moves(
                    service, "folder-{}".format(failure)
                )
                by_path = os.path.join(
                    os.path.realpath(path.parent), path.name
                )
                read = mock.Mock(return_value=b"\x02\x00\x00\x00acl")
                if failure is not None:
                    read.side_effect = OSError(failure, os.strerror(failure))
                with (
                    linux,
                    no_proc,
                    mock.patch("os.getxattr", read, create=True),
                    mock.patch("os.setxattr", mock.Mock(), create=True),
                ):
                    with self.assertRaises(AccessNotKept):
                        self.client(service).file.download_file("a.bin", path)

                read.assert_called_once_with(
                    by_path, "system.posix_acl_access", follow_symlinks=False
                )
                self.assertEqual(replaced.read_bytes(), b"old content")
                self.assertEqual(sdk_entries(replaced.parent), [])

    def test_a_file_whose_owner_or_group_cannot_be_given_is_not_replaced(self):
        service = DownloadService(self, content(2500))
        path = self.existing()
        os.chown(path, -1, self.other_group())
        refused = PermissionError(errno.EPERM, "Operation not permitted")

        with (
            mock.patch("os.fchown", side_effect=refused),
            self.assertRaises(AccessNotKept) as caught,
        ):
            self.client(service).file.download_file("a.bin", path)

        self.assertIn("belongs to another group", str(caught.exception))
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])

    def test_a_linux_access_control_list_is_copied_or_the_file_is_not_replaced(
        self,
    ):
        # The Linux steps, where this system has no such lists to read.
        service = DownloadService(self, content(2500))
        linux = mock.patch.object(localfs, "sys", mock.Mock(platform="linux"))
        for failure, replaced in (
            (None, True),
            (errno.ENODATA, True),
            (errno.EACCES, False),
        ):
            with self.subTest(failure=failure):
                path = self.existing()
                written, removed = [], []
                read = mock.Mock(return_value=b"\x02\x00\x00\x00acl")
                if failure is not None:
                    read.side_effect = OSError(failure, os.strerror(failure))
                with (
                    linux,
                    mock.patch("os.getxattr", read, create=True),
                    mock.patch(
                        "os.setxattr",
                        lambda fd, name, value: written.append((name, value)),
                        create=True,
                    ),
                    mock.patch(
                        "os.removexattr",
                        lambda fd, name: removed.append(name),
                        create=True,
                    ),
                ):
                    if replaced:
                        self.client(service).file.download_file("a.bin", path)
                    else:
                        with self.assertRaises(AccessNotKept):
                            self.client(service).file.download_file(
                                "a.bin", path
                            )

                self.assertEqual(
                    read.call_args.args[1:], ("system.posix_acl_access",)
                )
                self.assertEqual(
                    path.read_bytes(),
                    service.content if replaced else b"old content",
                )
                expected = (
                    [("system.posix_acl_access", b"\x02\x00\x00\x00acl")]
                    if failure is None
                    else []
                )
                self.assertEqual(written, expected)
                # A file without a list replaced by one without a list either.
                self.assertEqual(
                    removed,
                    (
                        ["system.posix_acl_access"]
                        if failure == errno.ENODATA
                        else []
                    ),
                )
                self.assertEqual(self.stages(), [])

    def test_the_temporary_file_is_private_while_it_fills(self):
        import fcntl

        # A folder of this process's own and, on macOS, one whose access
        # control list lets everyone read and write every file and folder
        # made in it from now on, the SDK's included, holding an owner-only
        # file without a list of its own.
        folders = [("own", self.scratch)]
        if sys.platform == "darwin":
            shared = self.scratch / "shared"
            shared.mkdir()
            os.chmod(shared, 0o755)
            passed_on = "everyone allow read,write,execute,file_inherit,directory_inherit,only_inherit"
            subprocess.run(
                ["/bin/chmod", "+a", passed_on, shared], check=True, timeout=10
            )
            folders.append(("inherited", shared))
        real_open = os.open
        # Extended lists are observed on macOS; elsewhere only permissions.
        acl = self.acl_of if sys.platform == "darwin" else lambda _path: []

        for label, folder in folders:
            with self.subTest(label):
                service = DownloadService(self, content(5000))
                control = folder / "control.bin"
                control.write_bytes(b"")
                existing = folder / "existing.bin"
                existing.write_bytes(b"old content")
                os.chmod(existing, 0o600)
                if sys.platform == "darwin":
                    subprocess.run(
                        ["/bin/chmod", "-N", existing], check=True, timeout=10
                    )
                self.assertEqual(acl(existing), [])
                # Each file made in the SDK's directory the moment it was
                # made, and the directory then: a descriptor opened at that
                # moment would outlast any later change.
                created = []

                def observed(path, flags, mode=0o777, *, dir_fd=None):
                    handle = real_open(path, flags, mode, dir_fd=dir_fd)
                    if flags & os.O_CREAT and sys.platform == "darwin":
                        made = (
                            fcntl.fcntl(handle, fcntl.F_GETPATH, bytes(1024))
                            .rstrip(b"\0")
                            .decode()
                        )
                        directory = os.path.dirname(made)
                        if os.path.basename(directory).startswith(
                            ".files_sdk-"
                        ):
                            created.append(
                                (
                                    made.endswith(".files_sdk-download"),
                                    stat.S_IMODE(os.fstat(handle).st_mode),
                                    tuple(acl(made)),
                                    stat.S_IMODE(os.stat(directory).st_mode),
                                    tuple(acl(directory)),
                                )
                            )
                    return handle

                # And while the file fills.
                filling = []
                service.on_request = lambda _range: filling.extend(
                    (
                        name.endswith(".files_sdk-download"),
                        stat.S_IMODE(os.stat(folder / name).st_mode),
                        tuple(acl(folder / name)),
                    )
                    for name in sdk_entries(folder)
                )
                with mock.patch("os.open", observed):
                    self.client(service).file.download_file(
                        "a.bin", folder / "new.bin"
                    )
                    self.client(service).file.download_file("a.bin", existing)

                # The file owner-only in a directory only its owner can enter,
                # neither with an access control list.
                self.assertEqual(
                    set(filling), {(True, 0o600, ()), (False, 0o700, ())}
                )
                if sys.platform == "darwin":
                    self.assertEqual(
                        {entry[:3] for entry in created if entry[0]},
                        {(True, 0o600, ())},
                    )
                    self.assertEqual(
                        {entry[3:] for entry in created}, {(0o700, ())}
                    )
                # The replaced file keeps having no list and its permissions;
                # the new file gets what a new file there does.
                self.assertEqual(
                    (
                        existing.read_bytes(),
                        stat.S_IMODE(os.stat(existing).st_mode),
                        acl(existing),
                    ),
                    (service.content, 0o600, []),
                )
                self.assertEqual(
                    (
                        stat.S_IMODE(os.stat(folder / "new.bin").st_mode),
                        acl(folder / "new.bin"),
                    ),
                    (stat.S_IMODE(os.stat(control).st_mode), acl(control)),
                )
                if label == "inherited":
                    self.assertTrue(acl(control))
                self.assertEqual(sdk_entries(folder), [])

    def test_a_link_to_a_file_is_followed(self):
        data = content(2500)
        service = DownloadService(self, data)
        target = self.existing(name="target.bin")
        link = self.scratch / "link.bin"
        link.symlink_to(target)
        self.client(service).file.download_file("a.bin", link)
        self.assertTrue(link.is_symlink())
        self.assertEqual(target.read_bytes(), data)


class TestStageCapabilities(DownloadTestCase):
    """A stage does its work with or without the os functions some platforms
    lack: exact writes without os.pwrite (as on Windows), from several
    threads at once as a download's ranges write, a replaced file's
    permissions without os.fchmod (as on Windows before 3.13), and
    publishing by path names, without directories held open (as on
    Windows)."""

    def written(self, together=False, **patches):
        with localfs.Directory.open(str(self.scratch)) as parent:
            stage = localfs.Stage.create(parent, "a.bin")
            try:
                with mock.patch.dict(os.__dict__, patches):
                    for name in [
                        name
                        for name, value in patches.items()
                        if value is None
                    ]:
                        del os.__dict__[name]
                    # Apart, with a gap between, so that neither thread ever
                    # leaves the file's position where the other's next
                    # piece belongs.
                    writes = ((10, b"0123456789"), (0, b"abcde"))
                    if together:
                        threads = [
                            threading.Thread(target=stage.write_at, args=write)
                            for write in writes
                        ]
                        for thread in threads:
                            thread.start()
                        for thread in threads:
                            thread.join(10)
                        self.assertFalse(
                            any(thread.is_alive() for thread in threads)
                        )
                    else:
                        for offset, data in writes:
                            stage.write_at(offset, data)
                os.lseek(stage.fd, 0, os.SEEK_SET)
                return os.read(stage.fd, 20)
            finally:
                stage.discard()

    def test_writes_are_exact_with_or_without_positional_writes(self):
        real_write, real_pwrite, real_lseek = (
            os.write,
            getattr(os, "pwrite", None),
            os.lseek,
        )

        def short_write(fd, data):
            return real_write(fd, bytes(data[:3]))

        def short_pwrite(fd, data, offset):
            return real_pwrite(fd, bytes(data[:3]), offset)

        # Two threads write at once without os.pwrite. The first seek waits
        # for the other thread to seek too, which it can only do if a seek
        # and the write after it can be separated: the stage must keep them
        # together. Otherwise the first thread's next piece is written
        # wherever the other left the file's position, which is always
        # within the other's own bytes, never where the piece belongs, so
        # its own place is left empty.
        seeks = []
        other_seeked = threading.Event()

        def interleaving_lseek(fd, position, how):
            found = real_lseek(fd, position, how)
            seeks.append(position)
            if len(seeks) == 1:
                other_seeked.wait(0.5)
            else:
                other_seeked.set()
            return found

        cases = {
            "without pwrite": (False, {"pwrite": None, "write": short_write}),
            "without pwrite, from two threads at once": (
                True,
                {
                    "pwrite": None,
                    "write": short_write,
                    "lseek": interleaving_lseek,
                },
            ),
        }
        if real_pwrite is not None:
            cases["with pwrite"] = (False, {"pwrite": short_pwrite})
        for name, (together, patches) in cases.items():
            with self.subTest(name):
                self.assertEqual(
                    b"abcde" + bytes(5) + b"0123456789",
                    self.written(together, **patches),
                )
        # Both threads wrote in short pieces, each after a seek of its own.
        self.assertGreater(len(seeks), 2)
        self.assertEqual([], self.stages())

    @unittest.skipIf(sys.platform == "win32", "POSIX permissions")
    def test_publishing_keeps_the_replaced_files_permissions_without_fchmod(
        self,
    ):
        target = self.existing()
        os.chmod(target, 0o640)
        with localfs.Directory.open(str(self.scratch)) as parent:
            stage = localfs.Stage.create(parent, target.name)
            stage.write_at(0, b"new content")
            with mock.patch.dict(os.__dict__):
                del os.__dict__["fchmod"]
                stage.publish(target.name, confined=False)
        self.assertEqual(0o640, stat.S_IMODE(os.stat(target).st_mode))
        self.assertEqual(b"new content", target.read_bytes())
        self.assertEqual([], self.stages())

    def test_publishing_by_path_renames_the_closed_file_or_keeps_it_for_a_checkpoint(
        self,
    ):
        # Windows does not rename a file this process holds open, as os.open
        # opens it, nor replace one another program holds open; elsewhere
        # os.replace refuses them as Windows would.
        real_replace = os.replace
        held = []
        stage = None

        def windows_replace(source, destination):
            if sys.platform != "win32" and (
                stage.fd >= 0 or os.fspath(destination) in held
            ):
                raise PermissionError(
                    errno.EACCES,
                    "The process cannot access the file because it is being used by another process",
                )
            real_replace(source, destination)

        with (
            mock.patch.object(localfs, "ANCHORED", False),
            mock.patch("os.replace", windows_replace),
        ):
            for case, name, old, new in (
                ("a new file", "new.bin", None, b"new content"),
                ("an empty new file", "empty.bin", None, b""),
                ("a replaced file", "out.bin", b"old content", b"new content"),
            ):
                with self.subTest(case):
                    target = self.scratch / name
                    if old is not None:
                        self.existing(old, name)
                    with localfs.Directory.open(str(self.scratch)) as parent:
                        stage = localfs.Stage.create(parent, name)
                        stage.truncate(len(new))
                        stage.write_at(0, new)
                        stage.publish(name, confined=False)
                    self.assertEqual(new, target.read_bytes())
                    self.assertEqual([], self.stages())
            with self.subTest("a replaced file another program holds open"):
                target = self.existing(name="held.bin")
                # Owner-only: the temporary file takes these permissions,
                # and elsewhere than Windows only a private one is resumed.
                os.chmod(target, 0o600)
                with localfs.Directory.open(str(self.scratch)) as parent:
                    stage = localfs.Stage.create(parent, target.name)
                    recorded = stage.state()
                    stage.truncate(11)
                    stage.write_at(0, b"new content")
                    with open(target, "rb"):
                        held.append(os.fspath(target))
                        with self.assertRaises(PermissionError):
                            stage.publish(target.name, confined=False)
                    held.clear()
                    self.assertEqual(b"old content", target.read_bytes())
                    # Kept for a checkpoint, as a failed download keeps it.
                    stage.sync()
                    stage.keep()
                self.assertEqual(
                    [os.path.join(recorded["directory"], recorded["name"])],
                    self.stage_files(),
                )
                self.assertEqual(b"old content", target.read_bytes())
                # A later attempt resumes the same file, still private, and
                # publishes it, leaving nothing behind.
                with localfs.Directory.open(str(self.scratch)) as parent:
                    stage = localfs.Stage.adopt(parent, recorded, 11)
                    self.assertIsNotNone(stage)
                    stage.publish(target.name, confined=False)
                self.assertEqual(b"new content", target.read_bytes())
                self.assertEqual([], self.stages())


class TestDownloadLimits(DownloadTestCase):
    def test_a_stream_download_holds_its_ranges_within_a_shared_limiter(self):
        data = content(12000)
        service = DownloadService(self, data)
        limiter = files_sdk.TransferLimiter(max_parts=2, max_bytes=2 * RANGE)
        output = io.BytesIO()
        seen = []

        def record(header):
            start = int(header[len("bytes=") :].split("-")[0])
            seen.append(
                (
                    limiter.parts_in_use,
                    limiter.bytes_in_use,
                    start - output.tell(),
                )
            )

        service.on_request = record
        # The range next in turn is slow, so later ones wait, held, for it.
        service.delay = lambda start: 0.2 if start == RANGE else 0.0
        client = self.client(service, transfer_limiter=limiter)
        client.file.download_stream("a.bin", output, max_concurrency=4)
        self.assertEqual(output.getvalue(), data)
        self.assertLessEqual(max(parts for parts, _held, _ahead in seen), 2)
        self.assertLessEqual(
            max(held for _parts, held, _ahead in seen), 2 * RANGE
        )
        # No range starts more than the limiter's worth ahead of what the
        # stream has been given.
        self.assertLessEqual(
            max(ahead for _parts, _held, ahead in seen), 2 * RANGE
        )
        self.assertEqual((limiter.parts_in_use, limiter.bytes_in_use), (0, 0))

    def test_downloads_sharing_a_limiter_stay_within_its_parts(self):
        data = content(20000)
        service = DownloadService(self, data)
        limiter = files_sdk.TransferLimiter(max_parts=3)
        service.delay = lambda start: 0.01
        clients = [
            self.client(service, transfer_limiter=limiter) for _ in range(3)
        ]
        errors = []

        def download(client, index):
            try:
                client.file.download_file(
                    "a.bin",
                    self.scratch / "{}.bin".format(index),
                    max_concurrency=4,
                )
            except Exception as error:  # pragma: no cover - reported below
                errors.append(error)

        threads = [
            threading.Thread(target=download, args=(c, i))
            for i, c in enumerate(clients)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(errors, [])
        for index in range(3):
            self.assertEqual(
                (self.scratch / "{}.bin".format(index)).read_bytes(), data
            )
        self.assertLessEqual(service.max_active, 3)
        self.assertEqual((limiter.parts_in_use, limiter.bytes_in_use), (0, 0))

    def test_a_range_waiting_to_be_fetched_again_keeps_its_room_but_not_its_slot(
        self,
    ):
        # Two downloads share a limiter of one slot. The first's only range
        # is answered 503 asking for two seconds. While it waits to be
        # fetched again it keeps the room its bytes need, but not the slot,
        # which the second download uses for every one of its ranges
        # meanwhile, within the limiter's slot and bytes. Then the first is
        # fetched again and completes; or, cancelled while it waits, it stops,
        # its local file as it was, and gives everything back.
        limiter = files_sdk.TransferLimiter(max_parts=1, max_bytes=8 * RANGE)
        for cancelled in (False, True):
            with self.subTest(cancelled=cancelled):
                first_data, second_data = content(RANGE, seed=1), content(
                    4 * RANGE, seed=2
                )
                first, second = DownloadService(
                    self, first_data
                ), DownloadService(self, second_data)
                first.fail(0, status=503, retry_after=2)
                asked = threading.Event()
                first.on_request = lambda _header, asked=asked: asked.set()
                seen = []
                second.on_request = lambda _header, seen=seen: seen.append(
                    (
                        time.monotonic(),
                        limiter.parts_in_use,
                        limiter.bytes_in_use,
                    )
                )
                token = files_sdk.CancellationToken()
                path = self.existing(name="first.bin")
                first_client = self.client(first, transfer_limiter=limiter)
                second_client = self.client(second, transfer_limiter=limiter)
                errors = []

                def download_first(
                    client=first_client, path=path, token=token, errors=errors
                ):
                    try:
                        client.file.download_file(
                            "a.bin", path, {"cancel_token": token}
                        )
                    except Exception as error:
                        errors.append(error)

                thread = threading.Thread(target=download_first)
                thread.start()
                self.addCleanup(thread.join, 10)
                self.assertTrue(asked.wait(5))
                second_client.file.download_file(
                    "b.bin", self.scratch / "second.bin", max_concurrency=2
                )
                if cancelled:
                    token.cancel()
                thread.join(10)

                self.assertEqual(
                    second_data, (self.scratch / "second.bin").read_bytes()
                )
                self.assertEqual(4, len(seen))
                # Every range of the second took the one slot, while the
                # first's room stayed counted beside its own.
                self.assertEqual({1}, {parts for _at, parts, _bytes in seen})
                self.assertTrue(
                    all(
                        2 * RANGE <= held <= 8 * RANGE
                        for _at, _parts, held in seen
                    ),
                    seen,
                )
                if cancelled:
                    [error] = errors
                    self.assertIsInstance(error, OperationCancelledError)
                    self.assertEqual(b"old content", path.read_bytes())
                    self.assertEqual(["bytes=0-999"], first.ranges())
                else:
                    self.assertEqual([], errors)
                    self.assertEqual(first_data, path.read_bytes())
                    self.assertEqual(
                        ["bytes=0-999", "bytes=0-999"], first.ranges()
                    )
                    # All of the second's ranges came before the first was
                    # fetched again.
                    retried_at = first.storage_requests()[-1]["at"]
                    self.assertTrue(
                        all(at < retried_at for at, _parts, _bytes in seen),
                        (retried_at, seen),
                    )
                self.assertEqual(
                    (0, 0), (limiter.parts_in_use, limiter.bytes_in_use)
                )
                self.assertEqual(self.stages(), [])

    def test_request_slots_go_in_the_order_they_were_asked_for(self):
        # One slot and 350 bytes, shared as uploads and downloads share a
        # limiter, through the calls they make: an upload part asks for a
        # slot and its bytes together; a download range for its bytes, and
        # each attempt at it for a slot. A range holds 200 bytes and an
        # upload part 100 bytes and the slot.
        limiter = files_sdk.TransferLimiter(max_parts=1, max_bytes=350)
        stop = CancellationToken()
        lifetime = Lifetime(CancellationToken(), stop)
        threads, held, errors = [], [], []

        def settle():
            # On every exit, passing or failing: whatever still waits in
            # line stops, each thread ends, and all that was granted goes
            # back, so a regression is reported rather than left waiting.
            stop.cancel()
            for thread in threads:
                thread.join(5)
            for reservation in held:
                reservation.release()
            self.assertEqual(
                [], [thread.name for thread in threads if thread.is_alive()]
            )
            self.assertEqual(
                (0, 0, 0),
                (
                    limiter.parts_in_use,
                    limiter.bytes_in_use,
                    len(limiter._waiting),
                ),
            )

        self.addCleanup(settle)

        def holding(reservation):
            held.append(reservation)
            return reservation

        def asking(ask):
            """ask() on a thread of its own: an event set once it is
            granted, and what it was granted. Its error, if it fails, is
            kept for the test to report."""
            got, granted = [], threading.Event()

            def run():
                try:
                    got.append(holding(ask()))
                except BaseException as error:
                    errors.append(error)
                    return
                granted.set()

            thread = threading.Thread(target=run)
            threads.append(thread)
            thread.start()
            return granted, got

        def in_line(count):
            deadline = time.monotonic() + 5
            while (
                len(limiter._waiting) != count and time.monotonic() < deadline
            ):
                time.sleep(0.01)
            self.assertEqual(count, len(limiter._waiting))

        range_room = holding(_admitted(limiter, 200, lifetime, slot=False))
        part = holding(_admitted(limiter, 100, lifetime))
        # The range's attempt asks for the slot; then the upload prepares
        # its next part, which asks for the slot and 100 bytes. The slot
        # goes to the attempt, which asked first; the part waits.
        attempt_granted, attempt = asking(lambda: limiter._attempt(lifetime))
        in_line(1)
        next_part_granted, next_part = asking(
            lambda: _admitted(limiter, 100, lifetime)
        )
        in_line(2)
        part.release()
        self.assertTrue(attempt_granted.wait(5))
        self.assertFalse(next_part_granted.wait(0.2))
        self.assertEqual(
            (1, 200), (limiter.parts_in_use, limiter.bytes_in_use)
        )
        # Then room for 300 bytes more, and another attempt, ask after that
        # part. The part asked first, for the slot and room it can have:
        # it goes ahead of both.
        room_granted, room = asking(
            lambda: _admitted(limiter, 300, lifetime, slot=False)
        )
        in_line(2)
        second_granted, second = asking(lambda: limiter._attempt(lifetime))
        in_line(3)
        attempt[0].release()
        self.assertTrue(next_part_granted.wait(5))
        self.assertFalse(second_granted.wait(0.2))
        self.assertFalse(room_granted.wait(0))
        self.assertEqual(
            (1, 300), (limiter.parts_in_use, limiter.bytes_in_use)
        )
        # Once the part is done, the room asked for first cannot fit beside
        # the range's 200 bytes. The attempt behind it needs no room: it
        # takes the slot, so the range can finish and free its 200, and the
        # 300 then fit.
        next_part[0].release()
        self.assertTrue(second_granted.wait(5))
        self.assertFalse(room_granted.wait(0.2))
        self.assertEqual(
            (1, 200), (limiter.parts_in_use, limiter.bytes_in_use)
        )
        second[0].release()
        range_room.release()
        self.assertTrue(room_granted.wait(5))
        self.assertEqual(
            (0, 300), (limiter.parts_in_use, limiter.bytes_in_use)
        )
        room[0].release()
        # A range larger than max_bytes holds its room alone, and its
        # attempt, which needs no more, still gets the slot.
        oversized = holding(_admitted(limiter, 500, lifetime, slot=False))
        alone = holding(limiter._attempt(lifetime))
        self.assertEqual(
            (1, 500), (limiter.parts_in_use, limiter.bytes_in_use)
        )
        alone.release()
        oversized.release()
        for thread in threads:
            thread.join(5)
        self.assertEqual([], errors)
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))
        self.assertEqual(0, len(limiter._waiting))


class TestDownloadConcurrency(DownloadTestCase):
    """How many ranges a download bound to a version fetches at once, and
    how storage's pushback holds them back."""

    def test_an_s3_download_starts_at_the_scaled_target_within_its_cap_and_other_storage_stays_at_four(
        self,
    ):
        # Each range takes a while, so ranges overlap as much as the
        # download lets them. From S3 (the URL names an S3 endpoint, routed
        # to the local service), the scaled S3 policy's start of 150 ranges
        # at once, not the 4 of other storage nor a cap of 32 of its own;
        # max_concurrency caps it, and adaptive=False keeps it there.
        static = files_sdk.UploadTuning(adaptive=False)
        cases = (
            ("s3", True, {}, 400, 0.3, 33, 150, "scaled_s3"),
            (
                "s3 capped",
                True,
                {"max_concurrency": 40},
                200,
                0.3,
                33,
                40,
                "scaled_s3",
            ),
            (
                "s3 static",
                True,
                {"max_concurrency": 3, "tuning": static},
                30,
                0.05,
                2,
                3,
                "static",
            ),
            ("other storage", False, {}, 40, 0.05, 2, 4, "static"),
        )
        for name, s3, settings, ranges, delay, least, most, policy in cases:
            with self.subTest(name):
                data = content(ranges * RANGE)
                service = DownloadService(self, data)
                service.delay = lambda start, delay=delay: delay
                extra = {}
                if s3:
                    service.storage_origin = S3_ORIGIN
                    session = service.session()
                    self.addCleanup(session.close)
                    extra["http_session"] = session
                path = self.scratch / "{}.bin".format(name.replace(" ", "-"))
                with self.assertLogs("files_sdk", "INFO") as logs:
                    self.client(service, **extra).file.download_file(
                        "big.bin", path, **settings
                    )
                self.assertEqual(data, path.read_bytes())
                self.assertEqual(
                    {service.etag},
                    {
                        request["if_match"]
                        for request in service.storage_requests()
                    },
                )
                self.assertGreaterEqual(service.max_active, least)
                self.assertLessEqual(service.max_active, most)
                [finished] = [
                    line for line in logs.output if "Download finished" in line
                ]
                self.assertIn("concurrency={}".format(policy), finished)
                self.assertIn("peak_target={}".format(most), finished)
                self.assertEqual(self.stages(), [])

    def test_only_a_bound_download_from_an_s3_general_purpose_endpoint_takes_the_scaled_policy(
        self,
    ):
        # The policy a real download takes from the host of the URL Files.com
        # gave. Dual-stack path style, and a dotted bucket under
        # amazonaws.com.cn, are S3 general-purpose endpoints: the scaled S3
        # policy. A host with an endpoint label after another s3 label, and
        # S3 Transfer Acceleration, only resemble one: other storage's
        # policy. Without a download identity, an S3 general-purpose
        # endpoint's first answer binds the download to a version: a 206
        # from byte 0 with the file's size and a strong ETag, which every
        # later range carries in If-Match. The host alone grants nothing: a
        # weak ETag, storage that ignores Range, a redirect, which that first
        # request does not follow, or a host that only resembles S3's, and
        # the file is read in one response, following the redirect.
        data = content(3 * RANGE)
        first, s3 = (
            "bytes=0-{}".format(RANGE - 1),
            "https://bucket.s3.us-east-1.amazonaws.com",
        )
        cases = (
            (
                "https://s3.dualstack.eu-west-1.amazonaws.com",
                "if-match",
                {},
                "scaled_s3",
            ),
            (
                "https://my.bucket.s3.cn-north-1.amazonaws.com.cn",
                "if-match",
                {},
                "scaled_s3",
            ),
            (
                "https://a.s3.s3-us-east-1.amazonaws.com",
                "if-match",
                {},
                "static",
            ),
            (
                "https://bucket.s3-accelerate.amazonaws.com",
                "if-match",
                {},
                "static",
            ),
            (s3, "absent", {}, "scaled_s3"),
            (s3, "absent", {"etag_style": "weak"}, [first, None]),
            (s3, "absent", {"ignore_ranges": True}, [first, None]),
            (s3, "absent", {"redirect_to": s3}, [first, None, None]),
            (
                "https://bucket.s3-accelerate.amazonaws.com",
                "absent",
                {},
                [None],
            ),
        )
        for origin, identity, switches, policy in cases:
            with self.subTest(origin=origin, identity=identity, **switches):
                service = DownloadService(self, data)
                service.identity = identity
                service.storage_origin = origin
                for name, value in switches.items():
                    setattr(service, name, value)
                session = service.session()
                self.addCleanup(session.close)
                path = self.scratch / "classified.bin"
                with self.assertLogs("files_sdk", "INFO") as logs:
                    self.client(
                        service, http_session=session
                    ).file.download_file("a.bin", path)
                self.assertEqual(data, path.read_bytes())
                [finished] = [
                    line for line in logs.output if "Download finished" in line
                ]
                if isinstance(policy, list):
                    # Read whole: storage's first answer, if it was asked for
                    # one, bound nothing, and no request carried an If-Match.
                    self.assertEqual(policy, service.ranges())
                    self.assertEqual(
                        {None},
                        {
                            request["if_match"]
                            for request in service.storage_requests()
                        },
                    )
                    self.assertFalse(
                        any(
                            request["range"]
                            and "redirected=1" in request["query"]
                            for request in service.storage_requests()
                        )
                    )
                    self.assertIn("mode=whole", finished)
                    self.assertIn("pinned_version=False", finished)
                    self.assertNotIn("concurrency=scaled_s3", finished)
                else:
                    self.assertEqual(3, len(service.ranges()))
                    self.assertIn("concurrency={}".format(policy), finished)
                    self.assertIn(
                        "peak_target={}".format(
                            150 if policy == "scaled_s3" else 4
                        ),
                        finished,
                    )
                    self.assertIn("pinned_version=True", finished)
                if identity == "absent" and not isinstance(policy, list):
                    # The first range is asked for without a condition; every
                    # later one with the ETag storage's first answer showed.
                    [unconditioned, *conditioned] = service.storage_requests()
                    self.assertEqual(
                        (first, None),
                        (unconditioned["range"], unconditioned["if_match"]),
                    )
                    self.assertEqual(
                        [service.etag] * 2,
                        [request["if_match"] for request in conditioned],
                    )
                    self.assertIn("bound_by=storage", finished)

    def test_a_throttle_holds_ranges_back_from_its_headers_even_when_its_body_is_lost(
        self,
    ):
        # Two ranges at once with no pause of their own, so only storage's
        # Retry-After can hold ranges back. The first range is answered 503
        # or 504 asking for a second, and its body is lost. Storage answers
        # the second range, already admitted, only once the client has taken
        # in that throttle, witnessed at the real controller, so no place
        # frees for a new range before. The first range's retry and the new
        # third and fourth ranges are requested only once that second,
        # counted from then, is over. Without retries, the lost body is the
        # download's error, and the local file is left as it was.
        answered = Controller._answered
        throttles = []
        taken_in = []

        def witness(controller, permit, status=None, retry_after=None):
            before = time.monotonic()
            answered(controller, permit, status, retry_after)
            if status in (503, 504):
                throttles.append((before, status, retry_after))
                taken_in[-1].set()

        patcher = mock.patch.object(Controller, "_answered", witness)
        patcher.start()
        self.addCleanup(patcher.stop)
        tuning = files_sdk.UploadTuning(adaptive=False, backpressure_pause=0)
        data = content(4 * RANGE)
        for status, retries in ((503, 3), (503, 0), (504, 3), (504, 0)):
            with self.subTest(status=status, retries=retries):
                service = DownloadService(self, data)
                service.fail(0, status=status, retry_after=1, drop_body=True)
                throttles.clear()
                taken_in.append(threading.Event())

                def hold_the_second(header, event=taken_in[-1]):
                    if header == "bytes={}-{}".format(RANGE, 2 * RANGE - 1):
                        event.wait(5)

                service.on_request = hold_the_second
                path = self.existing()
                limiter = files_sdk.TransferLimiter()
                client = self.client(
                    service,
                    transfer_limiter=limiter,
                    max_network_retries=retries,
                )

                if retries:
                    client.file.download_file(
                        "a.bin", path, max_concurrency=2, tuning=tuning
                    )
                    self.assertEqual(data, path.read_bytes())
                else:
                    with self.assertRaises(APIConnectionError):
                        client.file.download_file(
                            "a.bin", path, max_concurrency=2, tuning=tuning
                        )
                    self.assertEqual(b"old content", path.read_bytes())
                self.assertEqual(
                    [(status, 1.0)],
                    [(code, hint) for _before, code, hint in throttles],
                )
                deadline = throttles[0][0] + 1.0
                # Every range requested after the first range's first
                # attempt, apart from the second's (admitted before).
                first, later = set(), []
                for request in service.storage_requests():
                    if (
                        request["range"] in ("bytes=0-999", "bytes=1000-1999")
                        and request["range"] not in first
                    ):
                        first.add(request["range"])
                    else:
                        later.append((request["at"], request["range"]))
                self.assertTrue(
                    all(at >= deadline for at, _range in later),
                    (deadline, later),
                )
                if retries:
                    self.assertEqual(
                        ["bytes=0-999", "bytes=2000-2999", "bytes=3000-3999"],
                        sorted(r for _at, r in later),
                    )
                self.assertEqual(
                    (0, 0), (limiter.parts_in_use, limiter.bytes_in_use)
                )
                self.assertEqual(self.stages(), [])


class TestDownloadLifecycle(DownloadTestCase):
    def test_cancelling_stops_the_ranges_and_leaves_the_destination(self):
        service = DownloadService(self, content(20000))
        token = files_sdk.CancellationToken()
        service.delay = lambda start: 0.05
        service.on_request = lambda _range: (
            token.cancel() if service.served > 3 else None
        )
        path = self.existing()
        started = time.monotonic()
        with self.assertRaises(OperationCancelledError):
            self.client(service).file.download_file(
                "a.bin", path, {"cancel_token": token}
            )
        self.assertLess(time.monotonic() - started, 5)
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])
        self.assertLess(len(service.ranges()), 20)

    @unittest.skipIf(
        sys.platform == "win32" or os.geteuid() == 0, "POSIX permissions"
    )
    def test_a_stopped_download_raises_the_stop_before_touching_the_destination(
        self,
    ):
        service = DownloadService(self, content(2500))
        locked = self.scratch / "locked"
        locked.mkdir()
        os.chmod(locked, 0o500)
        self.addCleanup(os.chmod, locked, 0o700)
        token = files_sdk.CancellationToken()
        token.cancel()
        # Not the file system's refusal: nothing is made in the directory.
        with self.assertRaises(OperationCancelledError):
            self.client(service).file.download_file(
                "a.bin", locked / "a.bin", {"cancel_token": token}
            )
        self.assertEqual(service.requests, [])
        self.assertEqual(os.listdir(locked), [])

    def test_progress_counts_committed_and_received_bytes(self):
        # Ranges of three chunks; the second is cut off after its first
        # chunk and a half, so one chunk is received twice.
        size = 3 * _CHUNK
        data = content(4 * size)
        service = DownloadService(self, data)
        service.short_once = {size}
        reports = []
        with mock.patch("files_sdk.download.DEFAULT_RANGE_SIZE", size):
            self.client(service).file.download_file(
                "a.bin", self.scratch / "a.bin", progress=reports.append
            )
        last = reports[-1]
        self.assertIsInstance(last, files_sdk.DownloadProgress)
        self.assertEqual(last.path, "a.bin")
        self.assertEqual(
            (last.total_bytes, last.bytes_committed, last.ranges_committed),
            (4 * size, 4 * size, 4),
        )
        self.assertEqual(last.bytes_received, 4 * size + _CHUNK)
        committed = [report.bytes_committed for report in reports]
        self.assertEqual(committed, sorted(committed))

    def test_a_failing_progress_callback_stops_the_download_with_its_error(
        self,
    ):
        service = DownloadService(self, content(20000))
        service.delay = lambda start: 0.05

        def fail(_progress):
            raise KeyError("stop")

        path = self.existing()
        with self.assertRaises(KeyError):
            self.client(service).file.download_file(
                "a.bin", path, progress=fail
            )
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])

        # Read in one response, the callback runs while the response is
        # read: its own error, even one from requests, is neither retried
        # nor taken for the download's.
        service = DownloadService(self, content(3 * _CHUNK))
        service.identity = "absent"
        own = requests.exceptions.ConnectionError(
            "the callback's own request failed"
        )

        def fail_with_requests(_progress):
            raise own

        with self.assertRaises(requests.exceptions.ConnectionError) as caught:
            self.client(service, max_network_retries=3).file.download_file(
                "a.bin", path, progress=fail_with_requests
            )
        self.assertIs(caught.exception, own)
        self.assertEqual(service.ranges(), [None])
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])

        # A callback that cancels the download and then raises: its own
        # error, not the cancellation, is what the download raises.
        service = DownloadService(self, content(3 * _CHUNK))
        service.identity = "absent"
        token = files_sdk.CancellationToken()
        after_cancelling = LookupError("the callback's own, after cancelling")

        def cancel_then_fail(_progress):
            token.cancel()
            raise after_cancelling

        with self.assertRaises(LookupError) as caught:
            self.client(service, max_network_retries=3).file.download_file(
                "a.bin",
                path,
                {"cancel_token": token},
                progress=cancel_then_fail,
            )
        self.assertIs(caught.exception, after_cancelling)
        self.assertTrue(token.cancelled)
        self.assertEqual(service.ranges(), [None])
        self.assertEqual(path.read_bytes(), b"old content")
        self.assertEqual(self.stages(), [])

    def test_text_is_decoded_across_range_boundaries(self):
        text = "é€" * 1500
        service = DownloadService(self, text.encode("utf-8"))
        with self.client(service).file.open("t.txt", "r") as remote:
            self.assertEqual(remote.read(), text)

    def test_a_file_keeps_its_url_and_identity_for_a_later_download(self):
        data = content(2500)
        service = DownloadService(self, data)
        file = self.client(service).file.download_file(
            "a.bin", self.scratch / "a.bin"
        )
        file.download_file(self.scratch / "again.bin")
        self.assertEqual((self.scratch / "again.bin").read_bytes(), data)
        self.assertEqual(service.issued, 1)
        self.assertEqual(
            {r["if_match"] for r in service.storage_requests()}, {service.etag}
        )

    def test_the_download_is_logged_without_its_url(self):
        service = DownloadService(self, content(2500))
        with self.assertLogs("files_sdk", "INFO") as logs:
            self.client(service).file.download_file(
                "a.bin", self.scratch / "a.bin"
            )
        finished = [
            line for line in logs.output if "Download finished" in line
        ]
        self.assertEqual(len(finished), 1)
        self.assertIn("mode=ranges", finished[0])
        self.assertIn("pinned_version=True", finished[0])
        self.assertNotIn("secret", "\n".join(logs.output))
        # Nor the version's token or entity tag.
        self.assertNotIn(service.etag.strip('"'), "\n".join(logs.output))
        self.assertNotIn(token_of(service.content), "\n".join(logs.output))


if __name__ == "__main__":
    unittest.main()

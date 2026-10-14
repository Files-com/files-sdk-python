import io
import os
import random
import tempfile
import threading
import time
import tracemalloc
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import requests

import files_sdk
from files_sdk.error import (
    APIError,
    InvalidParameterError,
    InvalidRequestError,
    NotImplementedError,
    OperationCancelledError,
)
from files_sdk.upload import MAX_BUFFERED_PART, _Grant, _Planner
from tests.upload_fixtures import EXPIRED, SIGNED, UploadService


class ShortReads(io.RawIOBase):
    """A stream that returns at most a few bytes per read, as pipes and
    sockets can."""

    def __init__(self, data, most=3):
        self.stream = io.BytesIO(data)
        self.most = most

    def readable(self):
        return True

    def readinto(self, buffer):
        chunk = self.stream.read(min(len(buffer), self.most))
        buffer[: len(chunk)] = chunk
        return len(chunk)


class OverLongReads:
    """A stream whose read() returns more bytes than asked for."""

    def __init__(self, data):
        self.data = data

    def read(self, size):
        chunk, self.data = self.data[: size * 3], self.data[size * 3 :]
        return chunk


class UploadTestCase(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)

    def client(self, service, **settings):
        client = files_sdk.Client(
            api_key="key",
            base_url=service.url,
            initial_network_retry_delay=0,
            **settings,
        )
        self.addCleanup(client.close)
        return client

    def local(self, data, name="data.bin"):
        path = self.scratch / name
        path.write_bytes(data)
        return path


class TestParallelUploads(UploadTestCase):
    def test_parts_overlap_finish_out_of_order_and_reassemble_exactly(self):
        service = UploadService(self, part_size=1000)
        data = random.Random(1).randbytes(9500)
        # Earlier parts take longer, so later ones finish first.
        service.on_put = lambda number: time.sleep(0.02 * (10 - number))

        static = files_sdk.UploadTuning(adaptive=False)
        file = self.client(service).file.upload_file(
            self.local(data), "big.bin", tuning=static
        )

        self.assertEqual(data, service.assembled())
        self.assertEqual("big.bin", file.path)
        self.assertEqual(4, service.max_active)
        finish = service.finishes[0]
        self.assertEqual(
            [tag["part"] for tag in finish["etags"]], list(range(1, 11))
        )
        self.assertEqual(len(data), finish["size"])
        # Each part was sent once, and one request asked for several parts.
        self.assertEqual(sorted(service.puts), list(range(1, 11)))
        self.assertTrue(
            any(begin.get("parts", 1) > 1 for begin in service.begins)
        )
        self.assertEqual(len(data), service.begins[0]["size"])

    def test_parts_go_one_at_a_time_in_order_unless_parallel_parts_are_allowed(
        self,
    ):
        for grant in ({"parallel_parts": False}, {"parallel_parts": None}):
            with self.subTest(grant=grant):
                service = UploadService(self, part_size=3, grant=grant)
                data = b"0123456789"

                self.client(service).file.upload_file(
                    self.local(data), "a.txt", max_concurrency=8
                )

                self.assertEqual(data, service.assembled())
                self.assertEqual(1, service.max_active)
                self.assertEqual([1, 2, 3, 4], service.puts)
                # Each part was asked for once, just before it was sent.
                self.assertEqual(
                    [None, 2, 3, 4],
                    [begin.get("part") for begin in service.begins],
                )
                self.assertTrue(
                    all("parts" not in begin for begin in service.begins)
                )

    def test_max_concurrency_one_sends_parts_one_at_a_time(self):
        service = UploadService(self, part_size=2)
        self.client(service).file.upload_file(
            self.local(b"abcdefg"), "a.txt", max_concurrency=1
        )
        self.assertEqual((1, [1, 2, 3, 4]), (service.max_active, service.puts))

    def test_an_empty_upload_sends_one_empty_part(self):
        service = UploadService(self)
        self.client(service).file.upload_file(self.local(b""), "empty.txt")
        self.assertEqual(([1], [b""]), (service.puts, service.attempts(1)))
        self.assertEqual(
            (0, 0), (service.begins[0]["size"], service.finishes[0]["size"])
        )

    def test_a_failed_part_is_sent_again_with_the_same_bytes(self):
        service = UploadService(self, part_size=4)
        service.fail(2, status=503)
        service.hang_up(3)
        data = b"abcdefghijklmnop"

        self.client(service).file.upload_file(self.local(data), "a.txt")

        self.assertEqual([b"efgh", b"efgh"], service.attempts(2))
        self.assertEqual([b"ijkl", b"ijkl"], service.attempts(3))
        self.assertEqual([b"abcd"], service.attempts(1))
        self.assertEqual(data, service.assembled())
        self.assertEqual(1, len(service.finishes))

    def test_parts_are_not_sent_again_when_retry_parts_is_false(self):
        service = UploadService(
            self, part_size=4, grant={"retry_parts": False}
        )
        service.fail(2, status=503)

        with self.assertRaises(APIError) as caught:
            self.client(service).file.upload_file(
                self.local(b"abcdefghijkl"), "a.txt"
            )

        self.assertEqual(503, caught.exception.http_status)
        self.assertIn("started again", "\n".join(caught.exception.__notes__))
        self.assertEqual(
            "HTTP 503 Transfer request failed for the upload of a.txt",
            str(caught.exception),
        )
        self.assertEqual([b"efgh"], service.attempts(2))
        self.assertEqual([], service.finishes)

    def test_a_failed_part_stops_the_upload_without_completing_it(self):
        service = UploadService(self, part_size=4)
        service.fail(1, status=403)
        held = service.hold(2)

        def release_later():
            held.wait(5)
            time.sleep(0.05)
            service.release(2)

        threading.Thread(target=release_later).start()
        with self.assertRaises(APIError) as caught:
            self.client(service).file.upload_file(
                self.local(b"abcdefghijkl"), "a.txt"
            )

        self.assertEqual(403, caught.exception.http_status)
        self.assertEqual([], service.finishes)
        # The part in progress was stopped and its worker had finished.
        self.assertEqual(
            [],
            [
                t
                for t in threading.enumerate()
                if t.name.startswith("files_sdk upload")
            ],
        )

    def test_an_expired_part_url_is_renewed_for_the_same_part(self):
        service = UploadService(self, part_size=4)
        service.expire_first()
        data = b"abcdefghij"

        self.client(service).file.upload_file(self.local(data), "a.txt")

        self.assertEqual(data, service.assembled())
        # Every part went only to its renewed URL, as the same part.
        self.assertEqual(
            {"2"},
            {
                part.query["issue"]
                for parts in service.stored.values()
                for part in parts
            },
        )
        renewals = [
            begin
            for begin in service.begins
            if begin.get("ref") and begin.get("parts") is None
        ]
        self.assertEqual(
            sorted(begin["part"] for begin in renewals), [1, 2, 3]
        )

    def test_a_part_url_expired_by_its_own_signature_is_renewed_before_it_is_sent(
        self,
    ):
        for form in ("aws", "files", "google", "azure"):
            with self.subTest(form=form):
                service = UploadService(
                    self, part_size=4, storage_query="sig=a"
                )
                service.expire_first(
                    form
                )  # The description's expires time is still ahead.
                data = b"abcdefghij"

                self.client(service).file.upload_file(
                    self.local(data), "a.txt"
                )

                self.assertEqual(data, service.assembled())
                self.assertEqual(
                    {"2"},
                    {
                        part.query["issue"]
                        for parts in service.stored.values()
                        for part in parts
                    },
                )

    def test_a_part_url_that_expires_while_a_retry_waits_is_renewed_before_it_is_sent_again(
        self,
    ):
        # The first URL is signed for 62 seconds: fresh when first sent, but
        # within the minute of its expiry by the end of storage's Retry-After.
        lifetimes = iter([62])

        def signed(number):
            return (
                SIGNED["aws"](datetime.now(timezone.utc), next(lifetimes, 900))
                + "&sig=a"
            )

        service = UploadService(self, part_size=4, storage_query=signed)
        service.fail(1, status=503, retry_after=2)

        self.client(service).file.upload_file(self.local(b"abcd"), "a.txt")

        first, again = service.stored[1]
        self.assertEqual(
            ("1", "2"), (first.query["issue"], again.query["issue"])
        )
        self.assertEqual(
            (b"abcd", "4"), (again.body, again.headers["Content-Length"])
        )
        self.assertTrue(
            again.raw_query.endswith("&X-Amz-Expires=900&sig=a&issue=2")
        )
        # Renewed once its whole wait was over, for the same part of the same upload.
        (sent, _), (resent, _) = service.put_times
        self.assertGreaterEqual(resent - sent, 2)
        self.assertEqual(
            [None, ("upload-1", 1)],
            [
                begin.get("ref") and (begin["ref"], begin["part"])
                for begin in service.begins
            ],
        )
        self.assertEqual(b"abcd", service.assembled())

    def test_renewals_of_a_short_lived_url_stop_and_an_expired_one_is_never_sent_again(
        self,
    ):
        # Every URL is signed for 30 seconds, already within the minute of
        # expiry the SDK renews at, and storage keeps failing the part.
        def signed(number):
            return SIGNED["aws"](datetime.now(timezone.utc), 30) + "&sig=a"

        service = UploadService(self, part_size=4, storage_query=signed)
        service.fail(1, status=503, times=10)

        with self.assertRaises(APIError) as caught:
            self.client(service).file.upload_file(self.local(b"abcd"), "a.txt")

        # The first URL, expired as it waited, and one renewal after a
        # failure: each renewed URL went once, as given, and no expired one
        # went again.
        self.assertEqual(
            ["2", "3"], [part.query["issue"] for part in service.stored[1]]
        )
        self.assertEqual(3, service.issued[1])
        self.assertEqual(503, caught.exception.http_status)
        self.assertIn(
            "renewed as often as the SDK allows",
            "\n".join(caught.exception.__notes__),
        )
        self.assertEqual([], service.finishes)

    def test_a_part_storage_refuses_as_expired_is_renewed_and_sent_again_as_the_same_part(
        self,
    ):
        for provider, (status, body) in EXPIRED.items():
            with self.subTest(provider=provider):
                service = UploadService(
                    self, part_size=4, grant={"parallel_parts": False}
                )
                service.fail(2, status=status, body=body)
                data = b"abcdefghij"

                self.client(service).file.upload_file(
                    self.local(data), "a.txt"
                )

                self.assertEqual(data, service.assembled())
                self.assertEqual([1, 2, 2, 3], service.puts)
                first, again = service.stored[2]
                self.assertEqual(
                    (first.query["issue"], again.query["issue"]), ("1", "2")
                )
                self.assertEqual(first.body, again.body)
                # One renewal, of part 2 of the same upload, with the API key;
                # storage never sees it.
                self.assertEqual({1: 1, 2: 2, 3: 1}, dict(service.issued))
                self.assertEqual(
                    {"upload-1"},
                    {
                        begin["ref"]
                        for begin in service.begins
                        if begin.get("part") == 2
                    },
                )
                self.assertEqual({"key"}, {key for _, key in service.api_keys})
                self.assertNotIn("X-FilesAPI-Key", again.headers)
                self.assertEqual(
                    [tag["part"] for tag in service.finishes[0]["etags"]],
                    [1, 2, 3],
                )

    def test_a_part_refused_as_expired_again_and_again_stops_after_two_renewals(
        self,
    ):
        service = UploadService(self, part_size=4)
        status, body = EXPIRED["aws"]
        service.fail(1, status=status, times=5, body=body)

        with self.assertRaises(APIError) as caught:
            self.client(service).file.upload_file(self.local(b"abcd"), "a.txt")

        self.assertEqual(403, caught.exception.http_status)
        self.assertEqual([1, 1, 1], service.puts)
        self.assertEqual([], service.finishes)

    def test_a_part_refused_for_another_reason_is_not_renewed(self):
        service = UploadService(
            self, part_size=4, grant={"parallel_parts": False}
        )
        service.fail(
            2,
            status=403,
            body=b"<Error><Code>AccessDenied</Code><Message>Access Denied</Message></Error>",
        )

        with self.assertRaises(APIError) as caught:
            self.client(service).file.upload_file(
                self.local(b"abcdefghij"), "reports/a.txt"
            )

        self.assertEqual(403, caught.exception.http_status)
        self.assertEqual([1, 2], service.puts)
        self.assertEqual(1, service.issued[2])  # No renewal of part 2.
        self.assertEqual([], service.finishes)
        # The error names the file it was uploading; the storage answer and
        # URL stay out of it.
        self.assertEqual(
            "HTTP 403 Transfer request failed for the upload of reports/a.txt",
            str(caught.exception),
        )
        for private in ("AccessDenied", "/storage/", "issue="):
            self.assertNotIn(private, str(caught.exception))

    def test_a_part_refused_as_expired_is_not_renewed_when_parts_may_not_be_sent_again(
        self,
    ):
        service = UploadService(
            self, part_size=4, grant={"retry_parts": False}
        )
        status, body = EXPIRED["aws"]
        service.fail(1, status=status, body=body)

        with self.assertRaises(APIError) as caught:
            self.client(service).file.upload_file(self.local(b"abcd"), "a.txt")

        self.assertEqual([1], service.puts)
        self.assertEqual(1, service.issued[1])
        self.assertIn(
            "does not allow parts of this upload to be sent again",
            "".join(caught.exception.__notes__),
        )

    def test_a_renewal_that_changes_a_parts_size_stops_before_sending_it(self):
        service = UploadService(
            self, part_size=4, grant={"parallel_parts": False}
        )
        service.expire_first()
        original = service.describe

        def describe(ref, number):
            record = original(ref, number)
            if service.issued[number] > 1:
                record["partsize"] = 5  # The renewed description disagrees.
            return record

        service.describe = describe
        with self.assertRaises(InvalidRequestError) as caught:
            self.client(service).file.upload_file(
                self.local(b"abcdefgh"), "a.txt"
            )

        self.assertIn("changed the size of part 1", str(caught.exception))
        self.assertEqual([], service.puts)
        self.assertEqual([], service.finishes)

    def test_part_offsets_are_sent_on_every_part_when_granted(self):
        service = UploadService(
            self,
            part_size=4,
            grant={"part_offset_query": True},
            storage_query="b=2&sig=a%2Fb",
        )
        service.fail(2)

        self.client(service).file.upload_file(
            self.local(b"abcdefghij"), "a.txt"
        )

        offsets = {
            part.number: part.query["part_offset"]
            for parts in service.stored.values()
            for part in parts
        }
        self.assertEqual({1: "0", 2: "4", 3: "8"}, offsets)
        self.assertEqual(
            ["4", "4"],
            [part.query["part_offset"] for part in service.stored[2]],
        )
        # The signed query arrived exactly as given, with the offset after it.
        self.assertTrue(
            all(
                part.raw_query.startswith("b=2&sig=a%2Fb&issue=")
                for parts in service.stored.values()
                for part in parts
            )
        )

    def test_part_offsets_are_not_added_without_the_grant(self):
        service = UploadService(self, part_size=4)
        self.client(service).file.upload_file(self.local(b"abcdefgh"), "a.txt")
        self.assertTrue(
            all(
                "part_offset" not in part.query
                for parts in service.stored.values()
                for part in parts
            )
        )

    def test_part_headers_and_method_come_from_the_grant(self):
        service = UploadService(
            self,
            part_size=4,
            grant={"headers": {"x-ms-blob-type": "BlockBlob"}},
        )
        self.client(service).file.upload_file(self.local(b"abcdef"), "a.txt")
        self.assertTrue(
            all(
                part.headers.get("x-ms-blob-type") == "BlockBlob"
                for parts in service.stored.values()
                for part in parts
            )
        )
        self.assertTrue(
            all(
                "X-FilesAPI-Key" not in part.headers
                for parts in service.stored.values()
                for part in parts
            )
        )

    def test_unsupported_ways_of_sending_parts_fail_before_sending_anything(
        self,
    ):
        for grant in (
            {"parameters": {"key": "value"}},
            {"send": {"partdata": "form-field file"}},
            {"http_method": "COPY"},
        ):
            with self.subTest(grant=grant):
                service = UploadService(self, grant=grant)
                with self.assertRaises(NotImplementedError):
                    self.client(service).file.upload_file(
                        self.local(b"abcdefgh"), "a.txt"
                    )
                self.assertEqual(([], []), (service.puts, service.finishes))

    def test_a_later_part_that_withdraws_parallel_parts_stops_the_upload(self):
        service = UploadService(self, part_size=2)
        original = service.describe

        def describe(ref, number):
            record = original(ref, number)
            record["parallel_parts"] = number < 3
            return record

        service.describe = describe
        with self.assertRaises(files_sdk.error.APIConnectionError) as caught:
            self.client(service).file.upload_file(
                self.local(b"abcdefghij"), "a.txt", max_concurrency=2
            )
        self.assertIn("withdrew permission", str(caught.exception))
        self.assertNotIn(3, service.puts)
        self.assertEqual([], service.finishes)

    def test_upload_params_reach_begin_upload_and_the_completion(self):
        service = UploadService(self)
        for mkdir in (True, False):
            with self.subTest(mkdir_parents=mkdir):
                params = {
                    "mkdir_parents": mkdir,
                    "custom_metadata": {"team": "ops"},
                }
                self.client(service).file.upload_file(
                    self.local(b"abc"), "a/b.txt", params=params
                )
                self.assertEqual(mkdir, service.begins[-1]["mkdir_parents"])
                self.assertNotIn("custom_metadata", service.begins[-1])
                self.assertEqual(mkdir, service.finishes[-1]["mkdir_parents"])
                self.assertEqual(
                    {"team": "ops"}, service.finishes[-1]["custom_metadata"]
                )
                self.assertEqual(
                    {
                        "mkdir_parents": mkdir,
                        "custom_metadata": {"team": "ops"},
                    },
                    params,
                )

    def test_parameters_the_sdk_sets_are_refused_before_anything_is_sent(self):
        service = UploadService(self)
        with self.assertRaises(InvalidParameterError):
            self.client(service).file.upload_file(
                self.local(b"abc"), "a.txt", params={"ref": "other"}
            )
        self.assertEqual([], service.begins)

    def test_invalid_concurrency_and_progress_are_refused(self):
        service = UploadService(self)
        client = self.client(service)
        # An upload's cap goes up to the scaled S3 policy's maximum of 1024.
        for kwargs in (
            {"max_concurrency": 0},
            {"max_concurrency": 1025},
            {"max_concurrency": True},
            {"progress": 5},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(InvalidParameterError):
                    client.file.upload_file(
                        self.local(b"abc"), "a.txt", **kwargs
                    )
        self.assertEqual([], service.begins)


class TestUploadSources(UploadTestCase):
    def test_a_file_that_changes_while_it_uploads_is_not_completed(self):
        service = UploadService(
            self, part_size=4, grant={"parallel_parts": False}
        )
        local = self.local(b"abcdefghijkl")
        stat = local.stat()

        def rewrite(number):
            if number == 1:
                # Same size and modification time, different bytes.
                local.write_bytes(b"ABCDEFGHIJKL")
                os.utime(local, ns=(stat.st_atime_ns, stat.st_mtime_ns))

        service.on_put = rewrite
        with self.assertRaises(InvalidRequestError) as caught:
            self.client(service).file.upload_file(local, "a.txt")

        self.assertIn(
            "changed while it was being uploaded", str(caught.exception)
        )
        self.assertEqual(
            [b"abcd"],
            [part.body for parts in service.stored.values() for part in parts],
        )
        self.assertEqual([], service.finishes)

    def test_a_retried_part_sends_the_bytes_first_read_even_if_the_file_changes(
        self,
    ):
        service = UploadService(self, part_size=4)
        local = self.local(b"abcdefgh")
        service.fail(1, status=503)

        def rewrite(number):
            if number == 1 and len(service.stored[1]) == 1:
                local.write_bytes(b"ABCDEFGH")

        service.on_put = rewrite
        with self.assertRaises(InvalidRequestError):
            self.client(service).file.upload_file(
                local, "a.txt", max_concurrency=1
            )
        self.assertEqual([b"abcd", b"abcd"], service.attempts(1))
        self.assertEqual([], service.finishes)

    def test_a_stream_uploads_exactly_its_size_from_where_it_is(self):
        service = UploadService(self, part_size=4)
        stream = io.BytesIO(b"skip:0123456789tail")
        stream.seek(5)

        file = self.client(service).file.upload_stream(stream, "s.txt", 10)

        self.assertEqual(b"0123456789", service.assembled())
        self.assertEqual("s.txt", file.path)
        self.assertEqual(15, stream.tell())
        self.assertFalse(stream.closed)
        self.assertNotIn("provided_mtime", service.finishes[0])

    def test_short_reads_continue_until_the_part_is_full(self):
        service = UploadService(self, part_size=5)
        data = bytes(range(23))
        self.client(service).file.upload_stream(
            ShortReads(data), "s.bin", len(data)
        )
        self.assertEqual(data, service.assembled())
        self.assertEqual(
            [5, 5, 5, 5, 3], [len(service.part(n)) for n in range(1, 6)]
        )

    def test_bytes_a_stream_returns_beyond_what_was_asked_are_kept_for_the_next_part(
        self,
    ):
        service = UploadService(
            self, part_size=4, grant={"parallel_parts": False}
        )
        limiter = files_sdk.TransferLimiter(max_parts=2, max_bytes=64)
        data = b"abcdefghijklmnopqrst"
        self.client(service, transfer_limiter=limiter).file.upload_stream(
            OverLongReads(data), "s.txt", len(data)
        )
        self.assertEqual(data, service.assembled())
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))

    def test_a_stream_that_ends_early_fails_without_completing(self):
        service = UploadService(self, part_size=4)
        with self.assertRaises(InvalidRequestError) as caught:
            self.client(service).file.upload_stream(
                io.BytesIO(b"abcdef"), "s.txt", 10
            )
        self.assertIn(
            "ended after 6 bytes, before the 10 bytes", str(caught.exception)
        )
        self.assertEqual([], service.finishes)
        self.assertNotIn(2, service.puts)

    def test_a_stream_with_no_data_ready_or_text_fails_before_sending(self):
        class NoData(io.RawIOBase):
            def readable(self):
                return True

            def readinto(self, buffer):
                return None

        for stream, message in (
            (NoData(), "read() returned None"),
            (io.StringIO("abc"), "binary mode"),
        ):
            with self.subTest(stream=stream):
                service = UploadService(self)
                with self.assertRaises(InvalidParameterError) as caught:
                    self.client(service).file.upload_stream(stream, "s.txt", 3)
                self.assertIn(message, str(caught.exception))
                self.assertEqual([], service.puts)
                self.assertFalse(stream.closed)

    def test_an_invalid_size_is_refused(self):
        service = UploadService(self)
        for size in (-1, 1.5, "10", True):
            with self.subTest(size=size):
                with self.assertRaises(InvalidParameterError):
                    self.client(service).file.upload_stream(
                        io.BytesIO(b"abc"), "s.txt", size
                    )
        self.assertEqual([], service.begins)


class TestSharedLimits(UploadTestCase):
    def test_clients_sharing_a_limiter_stay_within_its_parts_and_bytes(self):
        service = UploadService(self, part_size=100)
        limiter = files_sdk.TransferLimiter(max_parts=3, max_bytes=250)
        seen = []

        def observe(number):
            seen.append((limiter.parts_in_use, limiter.bytes_in_use))
            time.sleep(0.01)

        service.on_put = observe
        clients = [
            self.client(service, transfer_limiter=limiter) for _ in range(2)
        ]
        data = [random.Random(n).randbytes(1000) for n in range(2)]
        paths = [
            self.local(content, "f{}.bin".format(n))
            for n, content in enumerate(data)
        ]
        errors = []

        def run(n):
            try:
                clients[n].file.upload_file(
                    paths[n], "f{}.bin".format(n), max_concurrency=4
                )
            except Exception as error:  # noqa: BLE001
                errors.append(error)

        threads = [threading.Thread(target=run, args=(n,)) for n in range(2)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(30)

        self.assertEqual([], errors)
        self.assertLessEqual(
            service.max_active, 2
        )  # 250 bytes hold two 100-byte parts
        self.assertTrue(
            all(parts <= 3 and held <= 250 for parts, held in seen)
        )
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))
        self.assertEqual(2, len(service.finishes))

    def test_concurrent_uploads_through_one_transport_keep_their_own_credentials(
        self,
    ):
        # Parts and requests of several uploads run on one Requests session
        # at once: each request carries its own upload's key, never another's.
        service = UploadService(self, part_size=100)
        service.on_put = lambda number: time.sleep(0.005)
        shared = requests.Session()
        self.addCleanup(shared.close)
        clients = [
            files_sdk.Client(
                api_key="clientkey{}".format(i),
                base_url=service.url,
                http_session=shared,
                initial_network_retry_delay=0,
            )
            for i in range(3)
        ]
        for client in clients:
            self.addCleanup(client.close)
        with mock.patch.multiple(
            files_sdk, base_url=service.url, the_api_key="modulekey"
        ):
            jobs = [
                (client.file.upload_file, "c{}.bin".format(i), {})
                for i, client in enumerate(clients)
            ]
            jobs += [
                (
                    files_sdk.upload_file,
                    "m{}.bin".format(i),
                    {"api_key": "optionkey{}".format(i)},
                )
                for i in range(3)
            ]
            errors = []

            def run(upload, destination, options):
                try:
                    upload(
                        self.local(bytes(1000), destination),
                        destination,
                        options,
                    )
                except Exception as error:  # pragma: no cover - reported below
                    errors.append(error)

            threads = [threading.Thread(target=run, args=job) for job in jobs]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()
        self.assertEqual(errors, [])
        expected = {
            "c{}.bin".format(i): "clientkey{}".format(i) for i in range(3)
        }
        expected.update(
            {"m{}.bin".format(i): "optionkey{}".format(i) for i in range(3)}
        )
        seen = {}
        for path, key in service.api_keys:
            destination = path.rsplit("/", 1)[-1]
            seen.setdefault(destination, set()).add(key)
        self.assertEqual(
            seen, {destination: {key} for destination, key in expected.items()}
        )
        self.assertEqual(len(service.finishes), 6)

    def test_a_part_larger_than_the_byte_limit_runs_alone(self):
        service = UploadService(self, part_size=10)
        limiter = files_sdk.TransferLimiter(max_parts=4, max_bytes=4)
        self.client(service, transfer_limiter=limiter).file.upload_file(
            self.local(b"x" * 35), "a.txt"
        )
        self.assertEqual(1, service.max_active)
        self.assertEqual(b"x" * 35, service.assembled())

    def test_cancelling_an_upload_waiting_for_the_limiter_frees_its_place(
        self,
    ):
        service = UploadService(self, part_size=4)
        limiter = files_sdk.TransferLimiter(max_parts=1)
        held = service.hold(1)
        first = self.client(service, transfer_limiter=limiter)
        second = self.client(service, transfer_limiter=limiter)
        results = {}

        def run(name, client, path, options=None):
            try:
                results[name] = client.file.upload_file(path, name, options)
            except Exception as error:  # noqa: BLE001
                results[name] = error

        running = threading.Thread(
            target=run, args=("first.txt", first, self.local(b"abcd", "a"))
        )
        running.start()
        held.wait(5)
        token = files_sdk.CancellationToken()
        waiting = threading.Thread(
            target=run,
            args=(
                "second.txt",
                second,
                self.local(b"efgh", "b"),
                {"cancel_token": token},
            ),
        )
        waiting.start()
        time.sleep(0.3)  # The second upload is waiting for the first's part.
        token.cancel()
        waiting.join(5)
        service.release(1)
        running.join(5)

        self.assertIsInstance(results["second.txt"], OperationCancelledError)
        self.assertFalse(results["second.txt"].remote_outcome_unknown)
        self.assertEqual("first.txt", results["first.txt"].path)
        self.assertEqual([1], service.puts)  # The second upload sent no part.
        self.assertEqual(
            ["first.txt"], [finish["path"] for finish in service.finishes]
        )
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))

    def test_invalid_limits_are_refused(self):
        for kwargs in (
            {"max_parts": 0},
            {"max_bytes": 0},
            {"max_parts": 1.5},
            {"max_bytes": True},
        ):
            with self.subTest(kwargs=kwargs):
                with self.assertRaises(InvalidParameterError):
                    files_sdk.TransferLimiter(**kwargs)


class TestUploadLifecycle(UploadTestCase):
    def test_cancelling_stops_parts_in_progress_and_does_not_complete(self):
        service = UploadService(self, part_size=4)
        held = service.hold(2)
        token = files_sdk.CancellationToken()

        def cancel_when_held():
            held.wait(5)
            token.cancel()

        threading.Thread(target=cancel_when_held).start()
        started = time.monotonic()
        with self.assertRaises(OperationCancelledError) as caught:
            self.client(service).file.upload_file(
                self.local(b"abcdefghijkl"), "a.txt", {"cancel_token": token}
            )

        self.assertLess(time.monotonic() - started, 5)
        self.assertFalse(caught.exception.remote_outcome_unknown)
        self.assertEqual([], service.finishes)

    def test_progress_counts_committed_bytes_and_every_byte_sent(self):
        service = UploadService(self, part_size=4)
        service.fail(2)
        reports = []
        caller = threading.get_ident()

        def progress(report):
            self.assertEqual(caller, threading.get_ident())
            reports.append(report)

        self.client(service).file.upload_file(
            self.local(b"abcdefghij"), "a.txt", progress=progress
        )

        last = reports[-1]
        self.assertEqual(
            (10, 10, 14, 3),
            (
                last.total_bytes,
                last.bytes_committed,
                last.bytes_sent,
                last.parts_committed,
            ),
        )
        self.assertEqual("a.txt", last.path)
        committed = [report.bytes_committed for report in reports]
        self.assertEqual(committed, sorted(committed))

    def test_a_failing_progress_callback_stops_the_upload_with_its_error(self):
        service = UploadService(self, part_size=4)
        failure = ValueError("stop")

        def progress(report):
            raise failure

        with self.assertRaises(ValueError) as caught:
            self.client(service).file.upload_file(
                self.local(b"abcdefghij"), "a.txt", progress=progress
            )

        self.assertIs(failure, caught.exception)
        self.assertEqual([], service.finishes)

    def test_the_module_functions_and_helpers_use_the_same_engine(self):
        service = UploadService(self, part_size=4)
        service.on_put = lambda number: time.sleep(0.05)
        with mock.patch.multiple(
            files_sdk, base_url=service.url, the_api_key="key"
        ):
            files_sdk.upload_file(
                str(self.local(b"abcdefghij")), "one.txt", max_concurrency=2
            )
            files_sdk.upload_stream(io.BytesIO(b"klmnop"), "two.txt", 6)
            files_sdk.upload_to_remote_server(
                str(self.local(b"qrst")), 7, "three.txt"
            )
        self.assertEqual(
            ["one.txt", "two.txt", "_/RemoteServers/7/three.txt"],
            [finish["path"] for finish in service.finishes],
        )
        self.assertEqual(2, service.max_active)


class TestRemoteFiles(UploadTestCase):
    def test_a_remote_file_sends_parts_as_they_fill_and_the_rest_on_close(
        self,
    ):
        service = UploadService(
            self, part_size=4, grant={"parallel_parts": False}
        )
        client = self.client(service)

        with client.file.open("notes.txt", "wb") as remote:
            self.assertEqual(10, remote.write(b"abcdefghij"))
            self.assertEqual([1, 2], service.puts)  # Full parts went at once.
            self.assertLessEqual(len(remote.io_obj.getvalue()), 4)
            remote.flush()
            self.assertEqual([1, 2], service.puts)

        self.assertEqual(b"abcdefghij", service.assembled())
        self.assertEqual(10, service.finishes[0]["size"])

    def test_a_remote_file_whose_upload_failed_sends_nothing_more(self):
        service = UploadService(
            self,
            part_size=4,
            grant={"parallel_parts": False, "retry_parts": False},
        )
        service.fail(1, status=500)
        remote = self.client(service).file.open("notes.txt", "wb")

        with self.assertRaises(APIError):
            remote.write(b"abcdefgh")
        for action in (lambda: remote.write(b"more"), remote.close):
            with self.assertRaises(InvalidRequestError):
                action()

        self.assertEqual(([1], []), (service.puts, service.finishes))

    def test_a_write_that_fails_in_a_with_block_is_the_error_the_block_raises(
        self,
    ):
        service = UploadService(
            self,
            part_size=4,
            grant={"parallel_parts": False, "retry_parts": False},
        )
        service.fail(1, status=500)
        failures = []

        with self.assertRaises(APIError) as caught:
            with self.client(service).file.open("notes.txt", "wb") as remote:
                try:
                    remote.write(b"abcdefgh")
                except APIError as error:
                    failures.append(error)
                    raise

        # The write's own error, naming the file, not one saying the upload
        # failed earlier; the file is closed without sending anything more.
        self.assertIs(caught.exception, failures[0])
        self.assertEqual(
            "HTTP 500 Transfer request failed for the upload of notes.txt",
            str(caught.exception),
        )
        self.assertTrue(remote.closed)
        self.assertTrue(remote.io_obj.closed)
        remote.close()
        with self.assertRaises(ValueError):
            remote.write(b"more")
        self.assertEqual(([1], []), (service.puts, service.finishes))

    def test_another_exception_leaving_a_with_block_closes_the_file_as_a_local_file_does(
        self,
    ):
        # A with block is not a transaction: as for a local file, what was
        # written is kept, so the upload completes. A write refused before
        # anything is sent, such as bytes to a text file, does not end it.
        service = UploadService(self, part_size=1024)

        with self.assertRaises(KeyError):
            with self.client(service).file.open("notes.txt", "w") as remote:
                with self.assertRaises(TypeError):
                    remote.write(b"bytes")
                remote.write("kept")
                raise KeyError("the caller's own")

        self.assertTrue(remote.closed)
        self.assertEqual(b"kept", service.assembled())
        self.assertEqual(1, len(service.finishes))

    def test_a_remote_file_whose_completion_answer_was_lost_is_not_completed_again(
        self,
    ):
        service = UploadService(self, part_size=4)
        service.finish_hang_up = True
        remote = self.client(service).file.open("notes.txt", "wb")
        remote.write(b"abc")

        with self.assertRaises(files_sdk.error.APIConnectionError) as caught:
            remote.close()
        self.assertTrue(caught.exception.remote_outcome_unknown)
        # Closed, as a file whose close() failed is: closing again, or
        # writing, sends nothing.
        self.assertTrue(remote.closed)
        remote.close()
        with self.assertRaises(ValueError):
            remote.write(b"more")

        self.assertEqual(1, len(service.finishes))

    def test_a_remote_text_file_is_sent_as_utf8(self):
        service = UploadService(self, part_size=1024)
        with self.client(service).file.open("notes.txt", "w") as remote:
            remote.write("café")
        self.assertEqual("café".encode("utf-8"), service.assembled())

    def test_a_part_size_beyond_what_the_source_has_sends_only_the_source(
        self,
    ):
        # begin_upload's part size is the most a part may hold, and can be
        # beyond any storage service's limit, as a remote server's can: a
        # part holds what the source has, whatever the source.
        data = b"abcdefgh"

        def remote_file(files):
            with files.open("u.bin", "wb") as remote:
                remote.write(data)

        for name, upload in (
            (
                "stream of known size",
                lambda files: files.upload_stream(
                    io.BytesIO(data), "u.bin", len(data)
                ),
            ),
            (
                "stream of unknown size",
                lambda files: files.upload_stream(io.BytesIO(data), "u.bin"),
            ),
            (
                "local file",
                lambda files: files.upload_file(self.local(data), "u.bin"),
            ),
            ("remote file", remote_file),
        ):
            with self.subTest(name):
                service = UploadService(self, part_size=1024**4)
                upload(self.client(service).file)
                self.assertEqual(data, service.assembled())

        with self.subTest("upload_chunks, continued"):
            service = UploadService(self, part_size=1024**4)
            files = self.client(service).file
            part, etags, _sent = files.upload_chunks(
                io.BytesIO(b"abcd"), "c.bin"
            )
            files.upload_chunks(io.BytesIO(b"efgh"), "c.bin", part, etags)
            self.assertEqual(
                [b"abcd", b"efgh"], [service.part(number) for number in (1, 2)]
            )

    def test_a_stream_part_beyond_what_the_sdk_holds_fails_before_it_is_read(
        self,
    ):
        # A stream's part is held whole until storage has it. One of more
        # than MAX_BUFFERED_PART fails the upload, before any of it is read
        # when the stream's size shows it.
        size = MAX_BUFFERED_PART + 1
        service = UploadService(self, part_size=size)
        stream = io.BytesIO(b"abcdefgh")

        with self.assertRaises(InvalidRequestError):
            self.client(service).file.upload_stream(stream, "big.bin", size)

        self.assertEqual(0, stream.tell())
        self.assertEqual(([], []), (service.puts, service.finishes))

    def test_an_upload_of_unknown_size_holds_at_most_max_buffered_part_of_a_part(
        self,
    ):
        # Its stream's size is not known, so it is read up to the bound: one
        # that ends there is the final part, and one with more fails the
        # upload, as does a remote file written past it.
        with mock.patch("files_sdk.upload.MAX_BUFFERED_PART", 8):
            service = UploadService(self, part_size=16)
            files = self.client(service).file
            files.upload_stream(io.BytesIO(b"abcdefgh"), "fits.bin")
            self.assertEqual(b"abcdefgh", service.assembled())

            def remote_file():
                with files.open("big.bin", "wb") as remote:
                    remote.write(b"abcdefghi")

            for name, upload in (
                (
                    "stream",
                    lambda: files.upload_stream(
                        io.BytesIO(b"abcdefghi"), "big.bin"
                    ),
                ),
                ("remote file", remote_file),
            ):
                with (
                    self.subTest(name),
                    self.assertRaises(InvalidRequestError),
                ):
                    upload()

        self.assertEqual(([1], 1), (service.puts, len(service.finishes)))

    def test_upload_chunks_reads_short_reads_into_full_parts(self):
        service = UploadService(
            self, part_size=4, grant={"parallel_parts": False}
        )
        client = self.client(service)
        data = bytes(range(10))
        part, etags, sent = client.file.upload_chunks(
            ShortReads(data, most=1), "c.bin"
        )
        self.assertEqual((10, [1, 2, 3]), (sent, service.puts))
        self.assertEqual([1, 2, 3], [tag["part"] for tag in etags])
        self.assertEqual(3, part.part_number)
        self.assertEqual([], service.finishes)


class TestPlanning(unittest.TestCase):
    def test_planning_a_multi_terabyte_upload_is_arithmetic_alone(self):
        # Files.com's current part sizes: 5 MiB, then growing to 36 MiB, then
        # 1 GiB parts once the file is large.
        MiB = 1024 * 1024
        schedule = [5] + [6] * 2 + [8] * 4 + [12] * 8 + [20] * 16 + [36] * 32
        sizes = (
            [size * MiB for size in schedule]
            + [36 * MiB] * 5000
            + [1024 * MiB] * 4937
        )
        size = 3 * 1024**4 + 12345  # A little over 3 TiB.

        tracemalloc.start()
        planner = _Planner(size)
        parts = 0
        while not planner.done:
            record = {
                "ref": "r",
                "part_number": planner.number,
                "partsize": sizes[planner.number - 1],
                "upload_uri": "u",
            }
            part = planner.place(_Grant.parse(None, record))
            parts += 1
        _current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        self.assertEqual(size, planner.offset)
        self.assertEqual(size, part.offset + part.length)
        self.assertLessEqual(parts, 10000)
        self.assertLess(peak, 1024 * 1024)


if __name__ == "__main__":
    unittest.main()

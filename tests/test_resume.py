import errno
import io
import json
import os
import random
import stat
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

import files_sdk
from files_sdk.checkpoint import CheckpointFile, digest
from files_sdk.error import (
    APIConnectionError,
    APIError,
    InvalidParameterError,
    InvalidRequestError,
    OperationCancelledError,
    TransferPausedError,
)
from tests.download_fixtures import DownloadService, sdk_entries, token_of
from tests.upload_fixtures import EXPIRED, SITE_DISABLED, UploadService

RANGE = 1000


def content(size, seed=1):
    return random.Random(seed).randbytes(size)


class ResumeTestCase(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)
        self.checkpoint = self.scratch / "transfer.checkpoint"
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

    def local(self, data, name="data.bin"):
        path = self.scratch / name
        path.write_bytes(data)
        return path

    def saved(self):
        return json.loads(self.checkpoint.read_text())

    def stages(self):
        return sdk_entries(self.scratch)

    def stage_files(self):
        return [
            name
            for name in self.stages()
            if name.endswith(".files_sdk-download")
        ]


class TestUploadResume(ResumeTestCase):
    def failed_first(self, service, source, **options):
        """Upload source one part at a time with part 7 failing for good,
        so parts 1 to 6 arrive and the upload stops."""
        service.fail(7, status=500, times=99)
        client = self.client(service, max_network_retries=0)
        with self.assertRaises(APIError):
            client.file.upload_file(
                source,
                "big.bin",
                max_concurrency=1,
                checkpoint=self.checkpoint,
                **options,
            )
        service._failures[7].clear()

    def test_a_failed_upload_resumes_sending_only_the_parts_that_did_not_arrive(
        self,
    ):
        data = content(9500)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        self.failed_first(service, source)
        state = self.saved()["state"]
        self.assertEqual(state["ref"], "upload-1")
        self.assertEqual(
            [row[4] for row in state["parts"]], [True] * 6 + [False]
        )
        before = len(service.puts)

        file = self.client(service).file.upload_file(
            source, "big.bin", checkpoint=self.checkpoint
        )

        self.assertEqual(file.path, "big.bin")
        self.assertEqual(service.assembled(), data)
        self.assertEqual(sorted(service.puts[before:]), [7, 8, 9, 10])
        self.assertEqual(service.begins[-1]["ref"], "upload-1")
        self.assertEqual(service.uploads, 1)
        self.assertEqual(len(service.finishes), 1)
        self.assertFalse(self.checkpoint.exists())
        self.assertFalse(Path(str(self.checkpoint) + ".lock").exists())

    def test_a_resumed_part_whose_url_storage_refuses_as_expired_is_renewed_without_resending_the_others(
        self,
    ):
        data = content(9500)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        self.failed_first(service, source)
        before = len(service.puts)
        issued = dict(service.issued)
        status, body = EXPIRED["aws"]
        service.fail(7, status=status, body=body)

        self.client(service).file.upload_file(
            source, "big.bin", max_concurrency=1, checkpoint=self.checkpoint
        )

        self.assertEqual(service.assembled(), data)
        self.assertEqual(service.puts[before:], [7, 7, 8, 9, 10])
        # Part 7 was described on resuming and once more when refused.
        self.assertEqual(
            [service.issued[n] - issued.get(n, 0) for n in range(1, 11)],
            [0] * 6 + [2, 1, 1, 1],
        )
        self.assertEqual(
            {begin.get("ref") for begin in service.begins[1:]}, {"upload-1"}
        )
        self.assertEqual(service.uploads, 1)
        self.assertEqual(
            [tag["part"] for tag in service.finishes[0]["etags"]],
            list(range(1, 11)),
        )
        self.assertFalse(self.checkpoint.exists())

    def test_the_checkpoint_is_private_and_holds_no_urls_or_credentials(self):
        service = UploadService(
            self, part_size=1000, storage_query="X-Amz-Signature=secret"
        )
        service.fail(3, status=500, times=99)
        client = files_sdk.Client(
            api_key="sdkkey", base_url=service.url, max_network_retries=0
        )
        self.addCleanup(client.close)
        with self.assertRaises(APIError):
            client.file.upload_file(
                self.local(content(9500)),
                "big.bin",
                max_concurrency=1,
                checkpoint=self.checkpoint,
            )
        text = self.checkpoint.read_text()
        # The site's origin, but no part URL, signature or API key.
        for secret in ("secret", "X-Amz", "/storage/", "issue=", "sdkkey"):
            self.assertNotIn(secret, text)
        if sys.platform != "win32":
            self.assertEqual(
                stat.S_IMODE(os.stat(self.checkpoint).st_mode), 0o600
            )

    def test_pausing_lets_parts_in_progress_finish_and_resuming_sends_the_rest(
        self,
    ):
        data = content(9500)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        pause = files_sdk.PauseToken()
        arrived = service.hold(3)

        def pause_then_release():
            arrived.wait(5)
            pause.pause()
            threading.Timer(0.3, service.release, [3]).start()

        threading.Thread(target=pause_then_release).start()
        static = files_sdk.UploadTuning(adaptive=False)
        with self.assertRaises(TransferPausedError) as caught:
            self.client(service).file.upload_file(
                source,
                "big.bin",
                max_concurrency=3,
                tuning=static,
                checkpoint=self.checkpoint,
                pause_token=pause,
            )
        self.assertEqual(caught.exception.checkpoint, str(self.checkpoint))
        self.assertEqual(service.finishes, [])
        # Part 3 was held, not stopped: it finished and counts.
        self.assertEqual(len(service.attempts(3)), 1)
        committed = {
            row[0] for row in self.saved()["state"]["parts"] if row[4]
        }
        self.assertIn(3, committed)

        self.client(service).file.upload_file(
            source, "big.bin", checkpoint=self.checkpoint, tuning=static
        )
        self.assertEqual(service.assembled(), data)
        for number in committed:
            self.assertEqual(len(service.attempts(number)), 1)
        self.assertFalse(self.checkpoint.exists())

    def change_once_pausing(self, service, source, replacement, pause):
        """Once part 3 arrives, held there, pause; then write replacement
        over source in place, keeping its size and modification time, and
        let part 3 finish. Returns the thread that does so."""
        arrived = service.hold(3)
        before = source.stat()

        def change():
            arrived.wait(5)
            pause.pause()
            with open(source, "r+b") as file:
                file.write(replacement)
            os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
            service.release(3)

        changer = threading.Thread(target=change)
        changer.start()
        self.addCleanup(changer.join, 10)
        return changer

    def test_a_file_that_changes_while_pausing_keeps_nothing_to_resume(self):
        # The parts that arrived hold bytes of the file as it was, which its
        # recorded size, times and identity cannot tell apart from what it
        # is now: the upload fails, its checkpoint keeps nothing to resume,
        # and the next call uploads the file as it is, in full.
        data, replacement = content(9500), content(9500, seed=2)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        pause = files_sdk.PauseToken()
        changer = self.change_once_pausing(service, source, replacement, pause)
        static = files_sdk.UploadTuning(adaptive=False)
        with self.assertRaisesRegex(
            InvalidRequestError, "changed while it was being uploaded"
        ):
            self.client(service).file.upload_file(
                source,
                "big.bin",
                max_concurrency=3,
                tuning=static,
                checkpoint=self.checkpoint,
                pause_token=pause,
            )
        changer.join(10)
        self.assertEqual(service.finishes, [])
        self.assertIsNone(self.saved()["state"])

        self.client(service).file.upload_file(
            source, "big.bin", checkpoint=self.checkpoint, tuning=static
        )
        self.assertEqual(service.assembled(), replacement)
        self.assertEqual(service.finishes[-1]["ref"], "upload-2")
        self.assertFalse(self.checkpoint.exists())

    def test_a_job_file_that_changes_while_pausing_keeps_nothing_to_resume(
        self,
    ):
        # The same in a job: that file fails, the job's checkpoint keeps no
        # state for it, and resuming the job uploads it as it is, in full.
        data, replacement = content(9500), content(9500, seed=2)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        pause = files_sdk.PauseToken()
        changer = self.change_once_pausing(service, source, replacement, pause)
        static = files_sdk.UploadTuning(adaptive=False)
        with self.assertRaises(TransferPausedError) as caught:
            self.client(service).file.upload_files(
                [(source, "big.bin")],
                max_concurrency=3,
                tuning=static,
                checkpoint=self.checkpoint,
                pause_token=pause,
            )
        changer.join(10)
        [failed] = caught.exception.result.failed
        self.assertIsInstance(failed.error, InvalidRequestError)
        self.assertIn("changed while it was being uploaded", str(failed.error))
        self.assertEqual(service.finishes, [])
        self.assertEqual(self.saved()["state"]["pending"], {})

        result = self.client(service).file.upload_files(
            [(source, "big.bin")], checkpoint=self.checkpoint, tuning=static
        )
        self.assertTrue(result.ok)
        self.assertEqual(service.completed("big.bin"), replacement)
        self.assertEqual(service.finishes[-1]["ref"], "upload-2")
        self.assertFalse(self.checkpoint.exists())

    def test_a_file_that_changes_as_a_part_fails_keeps_nothing_to_resume(self):
        # Part 1 has arrived and part 2 has been read and sent when the file
        # is written over in place, keeping its size and modification time,
        # and storage then refuses part 2 for good. The upload fails with
        # storage's error, and its checkpoint keeps nothing to resume: part
        # 1 holds the file's earlier bytes. The next call uploads the file
        # as it is, in full.
        data, replacement = content(3000), content(3000, seed=2)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        before = source.stat()

        def change(number):
            if number == 2:
                with open(source, "r+b") as file:
                    file.write(replacement)
                os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))

        service.on_put = change
        service.fail(2, status=500, times=99)
        with self.assertRaises(APIError) as caught:
            self.client(service, max_network_retries=0).file.upload_file(
                source,
                "big.bin",
                max_concurrency=1,
                checkpoint=self.checkpoint,
            )
        self.assertEqual(caught.exception.http_status, 500)
        # Part 1 arrived, and part 2 was read before the change.
        self.assertEqual(service.attempts(1), [data[:1000]])
        self.assertEqual(set(service.attempts(2)), {data[1000:2000]})
        self.assertEqual(service.finishes, [])
        self.assertIsNone(self.saved()["state"])

        service.on_put = None
        service._failures[2].clear()
        self.client(service).file.upload_file(
            source, "big.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(service.assembled(), replacement)
        self.assertEqual(
            [finish["ref"] for finish in service.finishes], ["upload-2"]
        )
        self.assertFalse(self.checkpoint.exists())

    def test_a_file_seen_to_change_by_a_call_paused_before_it_begins_keeps_nothing_to_resume(
        self,
    ):
        # Parts 1 to 6 arrived before part 7 failed for good. A call paused
        # before it begins sends nothing, but finds the file written over in
        # place, keeping its size and modification time, once it has looked
        # at it and opened its checkpoint: it fails, and the checkpoint keeps
        # nothing to resume, since parts 1 to 6 hold the file's earlier
        # bytes. The next call uploads the file as it is, in full.
        data, replacement = content(9500), content(9500, seed=2)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        self.failed_first(service, source)
        recorded = self.saved()["state"]
        self.assertEqual(
            (recorded["completion"], [row[4] for row in recorded["parts"]]),
            ("pending", [True] * 6 + [False]),
        )
        sent = (len(service.begins), len(service.puts), len(service.finishes))
        before = source.stat()
        open_checkpoint = CheckpointFile.open

        def open_then_write(checkpoint):
            state = open_checkpoint(checkpoint)
            with open(source, "r+b") as file:
                file.write(replacement)
            os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
            return state

        pause = files_sdk.PauseToken()
        pause.pause()
        with mock.patch.object(CheckpointFile, "open", open_then_write):
            with self.assertRaisesRegex(
                InvalidRequestError, "changed while it was being uploaded"
            ):
                self.client(service).file.upload_file(
                    source,
                    "big.bin",
                    checkpoint=self.checkpoint,
                    pause_token=pause,
                )
        self.assertEqual(
            (len(service.begins), len(service.puts), len(service.finishes)),
            sent,
        )
        self.assertIsNone(self.saved()["state"])

        self.client(service).file.upload_file(
            source, "big.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(service.assembled(), replacement)
        self.assertEqual(
            [finish["ref"] for finish in service.finishes], ["upload-2"]
        )
        self.assertFalse(self.checkpoint.exists())

    def test_cancelling_keeps_the_checkpoint_for_a_later_resume(self):
        data = content(9500)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        token = files_sdk.CancellationToken()
        service.on_put = lambda number: token.cancel() if number == 5 else None
        with self.assertRaises(OperationCancelledError):
            self.client(service).file.upload_file(
                source,
                "big.bin",
                {"cancel_token": token},
                max_concurrency=1,
                checkpoint=self.checkpoint,
            )
        self.assertTrue(self.checkpoint.exists())
        service.on_put = None
        self.client(service).file.upload_file(
            source, "big.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(service.assembled(), data)
        self.assertEqual(service.uploads, 1)

    def test_a_stream_upload_resumes_when_given_the_same_bytes_again(self):
        data = content(9500)
        service = UploadService(self, part_size=1000)
        service.fail(4, status=500, times=99)
        client = self.client(service, max_network_retries=0)
        with self.assertRaises(APIError):
            client.file.upload_stream(
                io.BytesIO(data),
                "s.bin",
                len(data),
                max_concurrency=1,
                checkpoint=self.checkpoint,
            )
        service._failures[4].clear()
        before = len(service.puts)

        with self.subTest("different bytes are refused"):
            changed = bytearray(data)
            changed[1500] ^= 0xFF
            with self.assertRaisesRegex(
                InvalidRequestError,
                "differ from those the checkpoint recorded",
            ):
                self.client(service).file.upload_stream(
                    io.BytesIO(bytes(changed)),
                    "s.bin",
                    len(data),
                    checkpoint=self.checkpoint,
                )
            self.assertEqual(len(service.puts), before)

        self.client(service).file.upload_stream(
            io.BytesIO(data), "s.bin", len(data), checkpoint=self.checkpoint
        )
        self.assertEqual(service.assembled(), data)
        self.assertEqual(sorted(service.puts[before:]), [4, 5, 6, 7, 8, 9, 10])

    def test_checking_the_parts_that_arrived_waits_for_room_in_a_shared_limiter(
        self,
    ):
        data = content(5000)
        service = UploadService(self, part_size=1000)
        service.fail(3, status=500, times=99)
        with self.assertRaises(APIError):
            self.client(service, max_network_retries=0).file.upload_stream(
                io.BytesIO(data),
                "s.bin",
                len(data),
                max_concurrency=1,
                checkpoint=self.checkpoint,
            )
        service._failures[3].clear()
        before = len(service.puts)
        # Room for two parts, but a part's 1000 bytes only alone.
        limiter = files_sdk.TransferLimiter(max_parts=2, max_bytes=500)
        other = UploadService(self, part_size=400)
        held = other.hold(1)
        holding = threading.Thread(
            target=self.client(
                other, transfer_limiter=limiter
            ).file.upload_file,
            args=(self.local(bytes(400), "o"), "o.bin"),
        )
        holding.start()
        self.addCleanup(holding.join, 10)
        held.wait(5)

        class Recording(io.BytesIO):
            reads = 0

            def read(self, size=-1):
                Recording.reads += 1
                return super().read(size)

        token = files_sdk.CancellationToken()
        threading.Timer(0.3, token.cancel).start()
        with self.assertRaises(OperationCancelledError):
            self.client(service, transfer_limiter=limiter).file.upload_stream(
                Recording(data),
                "s.bin",
                len(data),
                {"cancel_token": token},
                checkpoint=self.checkpoint,
            )
        # Nothing was read while the other upload held the room.
        self.assertEqual(0, Recording.reads)
        self.assertEqual(
            (1, 400), (limiter.parts_in_use, limiter.bytes_in_use)
        )
        self.assertTrue(self.checkpoint.exists())

        other.release(1)
        holding.join(10)
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))
        self.client(service, transfer_limiter=limiter).file.upload_stream(
            Recording(data), "s.bin", len(data), checkpoint=self.checkpoint
        )
        self.assertGreater(Recording.reads, 0)
        self.assertEqual(service.assembled(), data)
        self.assertEqual(sorted(service.puts[before:]), [3, 4, 5])
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))

    def test_a_spooled_stream_resumes_when_given_the_same_bytes_again(self):
        data = content(5500)
        service = UploadService(self, part_size=1000)
        service.fail(3, status=500, times=99)
        client = self.client(service, max_network_retries=0)
        options = {
            "spool_limit": 10000,
            "spool_directory": self.scratch,
            "checkpoint": self.checkpoint,
        }
        with self.assertRaises(APIError):
            client.file.upload_stream(
                io.BytesIO(data), "s.bin", max_concurrency=1, **options
            )
        service._failures[3].clear()
        before = len(service.puts)
        self.client(service).file.upload_stream(
            io.BytesIO(data), "s.bin", **options
        )
        self.assertEqual(service.assembled(), data)
        self.assertEqual(sorted(service.puts[before:]), [3, 4, 5, 6])
        self.assertEqual(
            [
                name
                for name in os.listdir(self.scratch)
                if name.startswith("files_sdk-upload-")
            ],
            [],
        )

    def test_a_file_changed_since_the_checkpoint_is_uploaded_again_in_full(
        self,
    ):
        service = UploadService(self, part_size=1000)
        source = self.local(content(9500))
        self.failed_first(service, source)
        replacement = content(9500, seed=2)
        source.write_bytes(replacement)
        self.client(service).file.upload_file(
            source, "big.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(service.assembled(), replacement)
        self.assertEqual(service.finishes[-1]["ref"], "upload-2")

    def test_an_upload_files_com_no_longer_has_starts_again(self):
        data = content(9500)
        service = UploadService(self, part_size=1000)
        source = self.local(data)
        self.failed_first(service, source)
        service.forget("upload-1")
        self.client(service).file.upload_file(
            source, "big.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(service.assembled(), data)
        self.assertEqual(service.finishes[-1]["ref"], "upload-2")

    def test_a_resumed_upload_whose_part_offsets_were_withdrawn_stops_before_sending(
        self,
    ):
        service = UploadService(
            self, part_size=1000, grant={"part_offset_query": True}
        )
        source = self.local(content(9500))
        self.failed_first(service, source)
        service.grant["part_offset_query"] = False
        before = len(service.puts)
        with self.assertRaisesRegex(
            APIConnectionError, "withdrew the part_offset"
        ):
            self.client(service).file.upload_file(
                source, "big.bin", checkpoint=self.checkpoint
            )
        self.assertEqual(len(service.puts), before)
        self.assertTrue(self.checkpoint.exists())

    def test_a_completion_whose_answer_was_lost_is_not_sent_again(self):
        service = UploadService(self, part_size=1000)
        source = self.local(content(3000))
        service.finish_hang_up = True
        with self.assertRaises(APIConnectionError) as first:
            self.client(service).file.upload_file(
                source, "f.bin", checkpoint=self.checkpoint
            )
        self.assertTrue(first.exception.remote_outcome_unknown)
        requests_before = len(service.begins)
        with self.assertRaises(APIConnectionError) as again:
            self.client(service).file.upload_file(
                source, "f.bin", checkpoint=self.checkpoint
            )
        self.assertTrue(again.exception.remote_outcome_unknown)
        self.assertIn("may have succeeded", str(again.exception))
        self.assertEqual(
            (len(service.finishes), len(service.begins)), (1, requests_before)
        )

        # The file is written over in place, keeping its size and
        # modification time, once a call has looked at it and opened its
        # checkpoint: that call still refuses, and the record of a completion
        # that may have happened is kept as it was.
        recorded = self.saved()
        self.assertEqual(recorded["state"]["completion"], "uncertain")
        before = source.stat()
        open_checkpoint = CheckpointFile.open

        def open_then_write(checkpoint):
            state = open_checkpoint(checkpoint)
            with open(source, "r+b") as file:
                file.write(content(3000, seed=2))
            os.utime(source, ns=(before.st_atime_ns, before.st_mtime_ns))
            return state

        with mock.patch.object(CheckpointFile, "open", open_then_write):
            with self.assertRaises(APIConnectionError) as written:
                self.client(service).file.upload_file(
                    source, "f.bin", checkpoint=self.checkpoint
                )
        self.assertTrue(written.exception.remote_outcome_unknown)
        self.assertIn("may have succeeded", str(written.exception))
        self.assertEqual(self.saved(), recorded)
        self.assertEqual(
            (len(service.finishes), len(service.begins)), (1, requests_before)
        )
        # Where the write left the identity the record holds as it was, as
        # it can on Windows, the record still applies: a later call refuses
        # too, sending nothing. Elsewhere the write changed the file's status
        # change time, so a later call takes it for another file.
        found = source.stat()
        if [
            found.st_dev,
            found.st_ino,
            found.st_size,
            found.st_mtime_ns,
            found.st_ctime_ns,
        ] == recorded["state"]["source"]["identity"]:
            with self.assertRaises(APIConnectionError) as later:
                self.client(service).file.upload_file(
                    source, "f.bin", checkpoint=self.checkpoint
                )
            self.assertTrue(later.exception.remote_outcome_unknown)
            self.assertIn("may have succeeded", str(later.exception))
            self.assertEqual(
                (len(service.finishes), len(service.begins)),
                (1, requests_before),
            )

    def test_the_completion_is_marked_on_disk_before_it_is_sent(self):
        service = UploadService(self, part_size=1000)
        source = self.local(content(3000))
        seen = []
        service.on_finish = lambda _path: seen.append(
            self.saved()["state"]["completion"]
        )
        self.client(service).file.upload_file(
            source, "f.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(seen, ["completing"])
        self.assertFalse(self.checkpoint.exists())

    @unittest.skipIf(
        sys.platform == "win32", "folders are not flushed on Windows"
    )
    def test_a_completion_mark_that_cannot_be_flushed_is_not_sent_and_stays_pending(
        self,
    ):
        service = UploadService(self, part_size=1000)
        source = self.local(content(3000))
        real_fsync = os.fsync
        refused = []

        def fsync(handle):
            # The checkpoint's folder refuses to be flushed once the mark is in it.
            if (
                stat.S_ISDIR(os.fstat(handle).st_mode)
                and self.saved()["state"]["completion"] == "completing"
            ):
                refused.append(handle)
                raise OSError(errno.EIO, os.strerror(errno.EIO))
            real_fsync(handle)

        with (
            mock.patch("os.fsync", fsync),
            self.assertRaises(OSError) as caught,
        ):
            self.client(service).file.upload_file(
                source, "f.bin", checkpoint=self.checkpoint
            )

        self.assertEqual(
            (caught.exception.errno, len(refused)), (errno.EIO, 1)
        )
        self.assertEqual(service.finishes, [])
        self.assertEqual(self.saved()["state"]["completion"], "pending")
        self.client(service).file.upload_file(
            source, "f.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(len(service.finishes), 1)
        self.assertEqual(service.completed("f.bin"), source.read_bytes())

    @unittest.skipIf(
        sys.platform == "win32", "folders are not flushed on Windows"
    )
    def test_an_upload_completes_where_the_file_system_cannot_flush_folders(
        self,
    ):
        service = UploadService(self, part_size=1000)
        source = self.local(content(3000))
        real_fsync = os.fsync
        refused = []

        def fsync(handle):
            if stat.S_ISDIR(os.fstat(handle).st_mode):
                refused.append(handle)
                raise OSError(errno.EINVAL, os.strerror(errno.EINVAL))
            real_fsync(handle)

        with mock.patch("os.fsync", fsync):
            self.client(service).file.upload_file(
                source, "f.bin", checkpoint=self.checkpoint
            )

        self.assertTrue(refused)
        self.assertEqual(len(service.finishes), 1)
        self.assertFalse(self.checkpoint.exists())

    def test_a_completion_answered_with_an_error_is_not_completed_again_on_resuming(
        self,
    ):
        # An error answer can come after Files.com completed the upload,
        # whatever its status or body, with retries left or none.
        for status, body, retries in (
            (422, None, None),
            (429, {}, 0),
            (503, {}, None),
        ):
            with self.subTest(status=status, body=body, retries=retries):
                service = UploadService(self, part_size=1000)
                source = self.local(content(3000))
                checkpoint = self.scratch / "completion-{}.checkpoint".format(
                    status
                )
                service.finish_status, service.finish_error = status, body
                settings = (
                    {} if retries is None else {"max_network_retries": retries}
                )
                with self.assertRaises(APIError) as caught:
                    self.client(service, **settings).file.upload_file(
                        source, "f.bin", checkpoint=checkpoint
                    )
                self.assertTrue(caught.exception.remote_outcome_unknown)
                self.assertEqual(
                    json.loads(checkpoint.read_text())["state"]["completion"],
                    "uncertain",
                )

                service.finish_status = 200
                with self.assertRaises(APIConnectionError) as resumed:
                    self.client(service).file.upload_file(
                        source, "f.bin", checkpoint=checkpoint
                    )
                self.assertTrue(resumed.exception.remote_outcome_unknown)
                self.assertEqual(len(service.finishes), 1)

    def test_a_completion_refused_while_the_site_is_disabled_is_completed_on_resuming(
        self,
    ):
        service = UploadService(self, part_size=1000)
        source = self.local(content(3000))
        service.finish_status, service.finish_error = 422, SITE_DISABLED
        with self.assertRaises(APIError) as caught:
            self.client(service).file.upload_file(
                source, "f.bin", checkpoint=self.checkpoint
            )
        # Files.com answered so before carrying out anything.
        self.assertFalse(caught.exception.remote_outcome_unknown)
        self.assertEqual(self.saved()["state"]["completion"], "pending")
        service.finish_status = 200
        self.client(service).file.upload_file(
            source, "f.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(len(service.finishes), 2)
        self.assertEqual(service.completed("f.bin"), source.read_bytes())

    def test_cancelling_after_the_mark_but_before_the_completion_is_sent_leaves_it_to_complete(
        self,
    ):
        service = UploadService(self, part_size=1000)
        source = self.local(content(3000))
        token = files_sdk.CancellationToken()
        real_replace = os.replace

        def cancel_once_marked(*args):
            # The mark is on disk the moment its file is renamed into place.
            if (
                os.fspath(args[1]) == str(self.checkpoint)
                and self.saved()["state"]["completion"] == "completing"
            ):
                token.cancel()

        def replace(*args, **kwargs):
            result = real_replace(*args, **kwargs)
            cancel_once_marked(*args)
            return result

        with mock.patch("os.replace", replace):
            with self.assertRaises(OperationCancelledError) as caught:
                self.client(service).file.upload_file(
                    source,
                    "f.bin",
                    {"cancel_token": token},
                    checkpoint=self.checkpoint,
                )
        self.assertFalse(caught.exception.remote_outcome_unknown)
        self.assertEqual(service.finishes, [])
        self.assertEqual(self.saved()["state"]["completion"], "pending")
        self.client(service).file.upload_file(
            source, "f.bin", checkpoint=self.checkpoint
        )
        self.assertEqual(len(service.finishes), 1)

    def test_a_completion_answered_with_an_unusable_success_is_not_completed_again(
        self,
    ):
        # Files.com completed the upload, but its answer cannot be used: no
        # proof it failed, so the upload stays possibly complete.
        for body in ([], b"not json"):
            with self.subTest(body=body):
                service = UploadService(self, part_size=1000)
                service.finish_body = body
                source = self.local(content(3000))
                checkpoint = self.scratch / "unusable-{}.checkpoint".format(
                    type(body).__name__
                )
                with self.assertRaises(APIConnectionError) as first:
                    self.client(service).file.upload_file(
                        source, "f.bin", checkpoint=checkpoint
                    )
                self.assertTrue(first.exception.remote_outcome_unknown)
                self.assertIn("may have taken effect", str(first.exception))
                self.assertNotIn("not json", str(first.exception))
                self.assertEqual(
                    json.loads(checkpoint.read_text())["state"]["completion"],
                    "uncertain",
                )
                begins = len(service.begins)
                with self.assertRaises(APIConnectionError) as again:
                    self.client(service).file.upload_file(
                        source, "f.bin", checkpoint=checkpoint
                    )
                self.assertTrue(again.exception.remote_outcome_unknown)
                self.assertEqual(
                    (len(service.finishes), len(service.begins)), (1, begins)
                )
                self.assertIn("f.bin", service.remote)

    def test_a_completion_answered_with_a_server_error_is_left_possibly_complete(
        self,
    ):
        # Unlike a refusal, a server error does not say the upload was not
        # completed.
        service = UploadService(self, part_size=1000)
        service.finish_status = 500
        source = self.local(content(3000))
        with self.assertRaises(APIError):
            self.client(service, max_network_retries=0).file.upload_file(
                source, "f.bin", checkpoint=self.checkpoint
            )
        self.assertEqual(self.saved()["state"]["completion"], "uncertain")
        service.finish_status = 200
        with self.assertRaises(APIConnectionError) as again:
            self.client(service).file.upload_file(
                source, "f.bin", checkpoint=self.checkpoint
            )
        self.assertTrue(again.exception.remote_outcome_unknown)
        self.assertEqual(len(service.finishes), 1)

    def test_a_job_completes_a_file_again_only_when_it_is_known_not_completed(
        self,
    ):
        # An unusable success, a lost answer or an error answer leaves the
        # file possibly complete, never completed again; the site-disabled
        # answer, or a stop before the request was sent, leaves it to
        # complete on the next run.
        for case in (
            "unusable success",
            "lost answer",
            "error answer",
            "site disabled",
            "stopped before sending",
        ):
            with self.subTest(case):
                service = UploadService(self, part_size=1000)
                name = case.replace(" ", "-")
                source = self.local(content(3000), name=name + ".bin")
                checkpoint = self.scratch / (name + ".checkpoint")
                token = files_sdk.CancellationToken()
                real_replace = os.replace

                def replace(*args, **kwargs):
                    result = real_replace(*args, **kwargs)
                    # The mark is on disk once the job's checkpoint says so.
                    if case == "stopped before sending" and os.fspath(
                        args[1]
                    ) == str(checkpoint):
                        [slot] = json.loads(checkpoint.read_text())["state"][
                            "pending"
                        ].values()
                        if slot["completion"] == "completing":
                            token.cancel()
                    return result

                service.finish_body = (
                    [] if case == "unusable success" else None
                )
                service.finish_hang_up = case == "lost answer"
                service.finish_status = (
                    422 if case in ("error answer", "site disabled") else 200
                )
                service.finish_error = (
                    SITE_DISABLED if case == "site disabled" else None
                )
                with mock.patch("os.replace", replace):
                    try:
                        result = self.client(service).file.upload_files(
                            [(source, "f.bin")],
                            {"cancel_token": token},
                            checkpoint=checkpoint,
                        )
                    except OperationCancelledError as stopped:
                        result = stopped.result  # type: ignore[attr-defined]
                [slot] = json.loads(checkpoint.read_text())["state"][
                    "pending"
                ].values()
                possibly_complete = case in (
                    "unusable success",
                    "lost answer",
                    "error answer",
                )
                self.assertEqual(
                    slot["completion"],
                    "uncertain" if possibly_complete else "pending",
                )
                self.assertFalse(result.completed)
                sent = len(service.finishes)
                (
                    service.finish_body,
                    service.finish_hang_up,
                    service.finish_status,
                ) = (None, False, 200)
                again = self.client(service).file.upload_files(
                    [(source, "f.bin")], checkpoint=checkpoint
                )
                if possibly_complete:
                    [failed] = again.failed
                    self.assertTrue(failed.error.remote_outcome_unknown)
                    self.assertEqual(len(service.finishes), sent)
                else:
                    self.assertTrue(again.ok)
                    self.assertEqual(len(service.finishes), sent + 1)
                    self.assertEqual(
                        service.completed("f.bin"), source.read_bytes()
                    )

    def test_a_process_killed_while_completing_is_not_completed_again(self):
        # The process dies after Files.com received the completion, before
        # its answer: only the mark saved before sending can tell.
        for route in ("file", "job"):
            with self.subTest(route):
                service = UploadService(self, part_size=1000)
                source = self.local(content(3000), name="{}.bin".format(route))
                checkpoint = self.scratch / "{}.checkpoint".format(route)
                child = {}

                def kill_before_answering(_path):
                    # On Windows kill() only starts the end of a process, so
                    # wait for this one to have ended before the answer is
                    # sent; a wait that runs out raises, and nothing answers.
                    process = child["process"]
                    process.kill()
                    process.wait(timeout=10)

                service.on_finish = kill_before_answering
                script = (
                    "import sys, files_sdk\n"
                    "client = files_sdk.Client(api_key='key', base_url=sys.argv[1], initial_network_retry_delay=0)\n"
                    "if sys.argv[4] == 'file':\n"
                    "    client.file.upload_file(sys.argv[2], 'f.bin', checkpoint=sys.argv[3])\n"
                    "else:\n"
                    "    client.file.upload_files([(sys.argv[2], 'f.bin')], checkpoint=sys.argv[3])\n"
                )
                child["process"] = subprocess.Popen(
                    [
                        sys.executable,
                        "-c",
                        script,
                        service.url,
                        str(source),
                        str(checkpoint),
                        route,
                    ],
                    cwd=os.getcwd(),
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                self.addCleanup(child["process"].kill)
                self.assertNotEqual(child["process"].wait(30), 0)
                self.assertEqual(len(service.finishes), 1)
                state = json.loads(checkpoint.read_text())["state"]
                if route == "file":
                    self.assertEqual(state["completion"], "completing")
                    with self.assertRaises(APIConnectionError) as again:
                        self.client(service).file.upload_file(
                            source, "f.bin", checkpoint=checkpoint
                        )
                    self.assertTrue(again.exception.remote_outcome_unknown)
                    self.assertIn("may have succeeded", str(again.exception))
                else:
                    [pending] = state["pending"].values()
                    self.assertEqual(pending["completion"], "completing")
                    result = self.client(service).file.upload_files(
                        [(source, "f.bin")], checkpoint=checkpoint
                    )
                    [failed] = result.failed
                    self.assertTrue(failed.error.remote_outcome_unknown)
                self.assertEqual(len(service.finishes), 1)

    def test_a_checkpoint_of_another_transfer_or_a_damaged_one_is_refused_before_any_request(
        self,
    ):
        service = UploadService(self, part_size=1000)
        source = self.local(content(9500))
        self.failed_first(service, source)
        requests = len(service.begins)
        with self.assertRaisesRegex(
            InvalidParameterError,
            "belongs to another transfer.*destination differs",
        ):
            self.client(service).file.upload_file(
                source, "other.bin", checkpoint=self.checkpoint
            )
        with self.assertRaisesRegex(InvalidParameterError, "params differ"):
            self.client(service).file.upload_file(
                source,
                "big.bin",
                params={"with_rename": True},
                checkpoint=self.checkpoint,
            )
        document = self.saved()
        document["state"]["ref"] = "upload-9"
        self.checkpoint.write_text(json.dumps(document))
        with self.assertRaisesRegex(
            InvalidRequestError, "incomplete or was changed"
        ):
            self.client(service).file.upload_file(
                source, "big.bin", checkpoint=self.checkpoint
            )
        self.checkpoint.write_text("{not json")
        with self.assertRaisesRegex(InvalidRequestError, "not JSON"):
            self.client(service).file.upload_file(
                source, "big.bin", checkpoint=self.checkpoint
            )
        self.assertEqual(len(service.begins), requests)

    @unittest.skipIf(
        sys.platform == "win32",
        "Windows gives no owners or permissions to check",
    )
    def test_an_upload_checkpoint_other_users_could_write_is_refused_before_any_request(
        self,
    ):
        service = UploadService(self, part_size=1000)
        source = self.local(content(9500))
        self.failed_first(service, source)
        sent = (len(service.begins), len(service.finishes))
        saved = self.checkpoint.read_bytes()
        os.chmod(self.checkpoint, 0o622)
        with self.assertRaisesRegex(
            InvalidRequestError, "can be changed by other users"
        ):
            self.client(service).file.upload_file(
                source, "big.bin", checkpoint=self.checkpoint
            )
        self.assertEqual((len(service.begins), len(service.finishes)), sent)
        self.assertEqual(self.checkpoint.read_bytes(), saved)

    def test_a_checkpoint_in_use_is_refused(self):
        service = UploadService(self, part_size=1000)
        source = self.local(content(3000))
        holder = CheckpointFile(str(self.checkpoint), "upload", {})
        holder.open()
        self.addCleanup(holder.close)
        with self.assertRaisesRegex(
            InvalidRequestError, "in use by another transfer"
        ):
            self.client(service).file.upload_file(
                source, "f.bin", checkpoint=self.checkpoint
            )
        self.assertEqual(service.begins, [])

    def test_invalid_pause_and_checkpoint_arguments_are_refused(self):
        service = UploadService(self, part_size=1000)
        client = self.client(service)
        source = self.local(content(100))
        with self.assertRaisesRegex(
            InvalidParameterError, "needs a checkpoint"
        ):
            client.file.upload_file(
                source, "f.bin", pause_token=files_sdk.PauseToken()
            )
        with self.assertRaises(InvalidParameterError):
            client.file.upload_file(
                source,
                "f.bin",
                pause_token=object(),
                checkpoint=self.checkpoint,
            )
        with self.assertRaises(InvalidParameterError):
            client.file.upload_file(source, "f.bin", checkpoint=42)
        with self.assertRaisesRegex(InvalidParameterError, "file of its own"):
            client.file.upload_file(source, "f.bin", checkpoint=source)
        with self.assertRaisesRegex(InvalidParameterError, "unknown size"):
            client.file.upload_stream(
                io.BytesIO(b"x"), "f.bin", checkpoint=self.checkpoint
            )
        self.assertEqual(service.begins, [])

    def test_progress_is_saved_while_a_part_takes_longer(self):
        data = content(6000)
        service = UploadService(self, part_size=1000)
        arrived = service.hold(3)
        static = files_sdk.UploadTuning(adaptive=False)
        done = threading.Event()

        def upload():
            try:
                self.client(service).file.upload_file(
                    self.local(data),
                    "slow.bin",
                    max_concurrency=3,
                    tuning=static,
                    checkpoint=self.checkpoint,
                )
            finally:
                done.set()

        worker = threading.Thread(target=upload)
        worker.start()
        self.addCleanup(worker.join)
        self.addCleanup(service.release_all)
        arrived.wait(5)
        # Nothing arrives while part 3 is held, yet the parts that arrived
        # before are saved within about a second.
        deadline = time.monotonic() + 5
        committed = set()
        while time.monotonic() < deadline and not {1, 2, 4, 5, 6} <= committed:
            time.sleep(0.1)
            committed = {
                row[0] for row in self.saved()["state"]["parts"] if row[4]
            }
        self.assertLessEqual({1, 2, 4, 5, 6}, committed)
        self.assertFalse(done.is_set())
        service.release(3)
        done.wait(10)
        self.assertEqual(service.assembled(), data)

    def test_a_paused_token_before_starting_sends_nothing(self):
        service = UploadService(self, part_size=1000)
        pause = files_sdk.PauseToken()
        pause.pause()
        with self.assertRaises(TransferPausedError):
            self.client(service).file.upload_file(
                self.local(content(100)),
                "f.bin",
                checkpoint=self.checkpoint,
                pause_token=pause,
            )
        self.assertEqual(service.begins, [])


class TestDownloadResume(ResumeTestCase):
    def failed_first(self, service, target, **options):
        """Download one range at a time with the range at 5000 failing for
        good, so ranges before it arrive and the download stops."""
        service.fail(5000, status=500, times=99)
        with self.assertRaises(APIError):
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin",
                target,
                max_concurrency=1,
                checkpoint=self.checkpoint,
                **options,
            )
        service.failures.clear()

    def test_a_failed_download_resumes_fetching_only_what_is_missing(self):
        data = content(9500)
        service = DownloadService(self, data)
        target = self.scratch / "a.bin"
        target.write_bytes(b"previous")
        self.failed_first(service, target)
        self.assertEqual(target.read_bytes(), b"previous")
        [stage] = self.stage_files()
        if sys.platform != "win32":
            self.assertEqual(
                stat.S_IMODE(os.stat(self.scratch / stage).st_mode), 0o600
            )
            self.assertEqual(
                stat.S_IMODE(
                    os.stat(self.scratch / os.path.dirname(stage)).st_mode
                ),
                0o700,
            )
        state = self.saved()["state"]
        self.assertEqual(state["written"], [[0, 4999]])
        # The version's token and size: never its URL or required headers.
        self.assertEqual(state["identity"], [token_of(data), 9500])
        text = self.checkpoint.read_text()
        self.assertNotIn("secret", text)
        self.assertNotIn(service.etag.strip('"'), text)
        before = len(service.ranges())

        self.client(service).file.download_file(
            "a.bin", target, checkpoint=self.checkpoint
        )

        self.assertEqual(target.read_bytes(), data)
        # Resuming renewed the same version before anything else.
        self.assertEqual(
            service.negotiations[-1].get("expected_download_identity"),
            token_of(data),
        )
        self.assertEqual(
            sorted(service.ranges()[before:]),
            sorted(
                "bytes={}-{}".format(s, min(s + RANGE, 9500) - 1)
                for s in range(5000, 9500, RANGE)
            ),
        )
        self.assertEqual(self.stages(), [])
        self.assertFalse(self.checkpoint.exists())

    def test_a_resumed_range_refused_as_expired_is_renewed_for_the_same_version(
        self,
    ):
        data = content(9500)
        service = DownloadService(self, data)
        target = self.scratch / "a.bin"
        self.failed_first(service, target)
        before = len(service.ranges())
        service.fail(
            5000, status=400, body=b"<Error><Code>ExpiredToken</Code></Error>"
        )

        self.client(service).file.download_file(
            "a.bin", target, max_concurrency=1, checkpoint=self.checkpoint
        )

        self.assertEqual(target.read_bytes(), data)
        # Renewed for the version the checkpoint named, on resuming and again after the refusal.
        self.assertEqual(
            [
                query.get("expected_download_identity")
                for query in service.negotiations[-2:]
            ],
            [token_of(data)] * 2,
        )
        expected = ["bytes=5000-5999"] + [
            "bytes={}-{}".format(s, min(s + RANGE, 9500) - 1)
            for s in range(5000, 9500, RANGE)
        ]
        self.assertEqual(service.ranges()[before:], expected)
        self.assertFalse(self.checkpoint.exists())

    def test_a_range_that_ran_long_left_the_ranges_it_did_not_own_to_resume_intact(
        self,
    ):
        # The second range is written first; then the first runs 64 bytes
        # long and the call fails. The checkpoint records the second range,
        # which must still hold its own bytes when the download resumes.
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

        target = self.scratch / "a.bin"
        with self.assertRaises(APIConnectionError):
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin",
                target,
                max_concurrency=2,
                progress=progress,
                checkpoint=self.checkpoint,
            )
        self.assertEqual(self.saved()["state"]["written"], [[1000, 1999]])
        [stage] = self.stage_files()
        self.assertEqual(
            (self.scratch / stage).read_bytes()[1000:], data[1000:]
        )
        before = len(service.ranges())
        self.client(service).file.download_file(
            "a.bin", target, checkpoint=self.checkpoint
        )
        self.assertEqual(target.read_bytes(), data)
        self.assertEqual(service.ranges()[before:], ["bytes=0-999"])

    def test_a_paused_download_resumes(self):
        data = content(20000)
        service = DownloadService(self, data)
        pause = files_sdk.PauseToken()
        service.delay = lambda start: 0.02
        service.on_request = lambda _range: (
            pause.pause() if service.served == 6 else None
        )
        target = self.scratch / "a.bin"
        with self.assertRaises(TransferPausedError):
            self.client(service).file.download_file(
                "a.bin", target, checkpoint=self.checkpoint, pause_token=pause
            )
        self.assertFalse(target.exists())
        written = self.saved()["state"]["written"]
        self.assertTrue(written)
        before = len(service.ranges())
        self.client(service).file.download_file(
            "a.bin", target, checkpoint=self.checkpoint
        )
        self.assertEqual(target.read_bytes(), data)
        # Nothing that arrived before is fetched again.
        self.assertLessEqual(
            len(service.ranges()) - before,
            20 - sum(e - s + 1 for s, e in written) // RANGE + 1,
        )

    def test_a_file_changed_since_the_checkpoint_is_downloaded_again_in_full(
        self,
    ):
        old = content(9500)
        service = DownloadService(self, old)
        target = self.scratch / "a.bin"
        self.failed_first(service, target)
        service.content = content(9500, seed=2)
        before = len(service.ranges())
        self.client(service).file.download_file(
            "a.bin", target, checkpoint=self.checkpoint
        )
        self.assertEqual(target.read_bytes(), service.content)
        self.assertEqual(self.stages(), [])
        # The renewal of the old version was refused, so every range of the
        # new one was fetched, none of the old kept.
        renewal, fresh = service.negotiations[-2:]
        self.assertEqual(
            renewal.get("expected_download_identity"), token_of(old)
        )
        self.assertNotIn("expected_download_identity", fresh)
        self.assertEqual(len(service.ranges()) - before, 10)

    def test_a_download_storage_bound_resumes_once_storage_confirms_its_version(
        self,
    ):
        # Without a download identity, from Amazon S3, the version is the one
        # storage's first answer bound the download to. Its checkpoint keeps
        # that version's ETag, size and storage resource digest, never the
        # URL, and nothing of it goes to Files.com: resuming asks for the
        # file's URL as any download without an identity does, and storage
        # confirms the version (its first byte, with If-Match) before only
        # the missing ranges are fetched. A file changed since is refused
        # there (412) and downloaded again in full, bound anew. Storage that
        # now ignores Range confirms the version with its whole file, which
        # is then read whole, with If-Match, as that version.
        for case in ("same", "changed", "ignores Range"):
            with self.subTest(case):
                changed = case == "changed"
                old = content(9500)
                service = DownloadService(self, old)
                session = service.bound_by_storage()
                self.addCleanup(session.close)
                etag = service.etag
                target = self.scratch / "{}.bin".format(case.replace(" ", "-"))
                service.fail(5000, status=500, times=99)
                with self.assertRaises(APIError):
                    self.client(
                        service, max_network_retries=0, http_session=session
                    ).file.download_file(
                        "a.bin",
                        target,
                        max_concurrency=1,
                        checkpoint=self.checkpoint,
                    )
                service.failures.clear()
                state = self.saved()["state"]
                self.assertEqual(state["written"], [[0, 4999]])
                self.assertEqual(state["storage"][:2], [etag, 9500])
                self.assertNotIn("identity", state)
                text = self.checkpoint.read_text()
                self.assertNotIn("secret", text)
                self.assertNotIn("storage/file", text)
                before = len(service.storage_requests())
                if changed:
                    service.content = content(9500, seed=2)
                service.ignore_ranges = case == "ignores Range"

                self.client(service, http_session=session).file.download_file(
                    "a.bin", target, checkpoint=self.checkpoint
                )

                self.assertEqual(target.read_bytes(), service.content)
                self.assertTrue(
                    all(
                        "expected_download_identity" not in query
                        for query in service.negotiations
                    )
                )
                resumed = service.storage_requests()[before:]
                self.assertEqual(
                    ("bytes=0-0", etag),
                    (resumed[0]["range"], resumed[0]["if_match"]),
                )
                if changed:
                    # Refused, then every range of the new version, its first
                    # without a condition, as a new download binds.
                    self.assertEqual(len(resumed), 11)
                    self.assertEqual(
                        ("bytes=0-{}".format(RANGE - 1), None),
                        (resumed[1]["range"], resumed[1]["if_match"]),
                    )
                    self.assertEqual(
                        {service.etag},
                        {request["if_match"] for request in resumed[2:]},
                    )
                elif case == "ignores Range":
                    # Confirmed by the whole file, then read whole once, as the version.
                    self.assertEqual(
                        [None],
                        [
                            request["range"]
                            for request in resumed
                            if request["range"] is None
                        ],
                    )
                    self.assertEqual(
                        {etag}, {request["if_match"] for request in resumed}
                    )
                else:
                    self.assertEqual(
                        sorted(request["range"] for request in resumed[1:]),
                        sorted(
                            "bytes={}-{}".format(s, min(s + RANGE, 9500) - 1)
                            for s in range(5000, 9500, RANGE)
                        ),
                    )
                    self.assertEqual(
                        {etag}, {request["if_match"] for request in resumed}
                    )
                self.assertEqual(self.stage_files(), [])
                self.assertFalse(self.checkpoint.exists())

    def test_a_replaced_temporary_file_is_not_trusted(self):
        data = content(9500)
        service = DownloadService(self, data)
        target = self.scratch / "a.bin"
        self.failed_first(service, target)
        [stage] = self.stage_files()
        path = self.scratch / stage
        original = os.stat(path)
        # Made while the original still exists, so it is another file (a file
        # made after the original is removed can reuse its inode), private as
        # the SDK's own, so only its identity tells them apart; then put in
        # its place.
        other = path.with_name("replacement")
        other.write_bytes(b"\0" * 9500)
        os.chmod(other, 0o600)
        os.replace(other, path)
        replacement = os.stat(path)
        self.assertNotEqual(
            (replacement.st_dev, replacement.st_ino),
            (original.st_dev, original.st_ino),
        )
        before = len(service.ranges())

        self.client(service).file.download_file(
            "a.bin", target, checkpoint=self.checkpoint
        )

        self.assertEqual(target.read_bytes(), data)
        # The download started again: what the checkpoint recorded was not used.
        self.assertIn(
            "bytes=0-{}".format(RANGE - 1), service.ranges()[before:]
        )
        # The replacement is not the SDK's, so it is left alone.
        self.assertEqual(self.stages(), [os.path.dirname(stage), stage])
        kept = os.stat(path)
        self.assertEqual(
            (kept.st_dev, kept.st_ino),
            (replacement.st_dev, replacement.st_ino),
        )
        self.assertEqual(path.read_bytes(), b"\0" * 9500)

    def test_a_temporary_file_others_could_have_opened_is_not_resumed(self):
        # Whoever opened it meanwhile could keep reading or writing it, so
        # the download starts again with a new one and the old is removed,
        # or on Windows left as it is. One still private resumes, also (on
        # macOS) in a folder whose access control list lets everyone use
        # every file and folder made in it. Windows permissions show only
        # whether a file is read-only, so there access control lists decide.
        # Each is downloaded into a folder of its own.
        if sys.platform == "win32":
            cases = [
                ("private", None),
                ("file list", lambda stage: icacls(stage, "*S-1-1-0:(R)")),
                (
                    "directory list",
                    lambda stage: icacls(stage.parent, "*S-1-1-0:(M)"),
                ),
            ]
        else:
            cases = [
                ("private", None),
                ("readable", lambda stage: os.chmod(stage, 0o644)),
                (
                    "directory mode",
                    lambda stage: os.chmod(stage.parent, 0o755),
                ),
            ]
        if sys.platform == "darwin":
            cases += [
                (
                    "file list",
                    lambda stage: acl("+a", "everyone allow read", str(stage)),
                ),
                (
                    "directory list",
                    lambda stage: acl(
                        "+a", "everyone allow list,search", str(stage.parent)
                    ),
                ),
            ]
        for label, expose in cases:
            with self.subTest(label):
                data = content(9500)
                service = DownloadService(self, data)
                name = label.replace(" ", "-")
                folder = self.scratch / name
                folder.mkdir()
                os.chmod(folder, 0o755)
                if sys.platform == "darwin" and expose is None:
                    acl(
                        "+a",
                        "everyone allow read,write,execute,file_inherit,directory_inherit,only_inherit",
                        str(folder),
                    )
                target, self.checkpoint = folder / "a.bin", self.scratch / (
                    name + ".checkpoint"
                )
                self.failed_first(service, target)
                [stage] = [
                    folder / name
                    for name in sdk_entries(folder)
                    if name.endswith(".files_sdk-download")
                ]
                if sys.platform == "darwin":
                    self.assertEqual(
                        (has_acl(stage), has_acl(stage.parent)), (False, False)
                    )
                if expose is not None:
                    expose(stage)
                left = (
                    sdk_entries(folder)
                    if expose is not None and sys.platform == "win32"
                    else []
                )
                before = len(service.ranges())

                self.client(service).file.download_file(
                    "a.bin", target, checkpoint=self.checkpoint
                )

                self.assertEqual(target.read_bytes(), data)
                # Ranges 5000 to 9499 when resumed, all ten when started again.
                self.assertEqual(
                    len(service.ranges()) - before, 5 if expose is None else 10
                )
                self.assertEqual(sdk_entries(folder), left)
                self.assertFalse(self.checkpoint.exists())

    def test_progress_is_saved_while_a_range_takes_longer(self):
        data = content(6000)
        service = DownloadService(self, data)
        blocker = threading.Event()
        self.addCleanup(blocker.set)
        service.on_request = lambda header: (
            blocker.wait(10) if header == "bytes=3000-3999" else None
        )
        target = self.scratch / "a.bin"
        worker = threading.Thread(
            target=lambda: self.client(service).file.download_file(
                "a.bin", target, max_concurrency=3, checkpoint=self.checkpoint
            )
        )
        worker.start()
        self.addCleanup(worker.join)
        deadline = time.monotonic() + 5
        written = []
        while time.monotonic() < deadline and written != [
            [0, 2999],
            [4000, 5999],
        ]:
            time.sleep(0.1)
            written = (
                self.saved()["state"]["written"]
                if self.checkpoint.exists()
                else []
            )
        self.assertEqual(written, [[0, 2999], [4000, 5999]])
        blocker.set()
        worker.join(10)
        self.assertEqual(target.read_bytes(), data)

    def test_a_download_that_wrote_nothing_keeps_no_checkpoint(self):
        service = DownloadService(self, content(5000))
        service.fail(0, status=500, times=99)
        target = self.scratch / "a.bin"
        # One range at a time, so the first fails before any other arrives.
        with self.assertRaises(APIError):
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", target, max_concurrency=1, checkpoint=self.checkpoint
            )
        self.assertFalse(self.checkpoint.exists())
        self.assertEqual(self.stages(), [])

    def test_a_stream_download_resumes_just_after_the_bytes_it_wrote(self):
        data = content(9500)
        service = DownloadService(self, data)
        service.fail(5000, status=500, times=99)
        output = io.BytesIO()
        with self.assertRaises(APIError):
            self.client(service, max_network_retries=0).file.download_stream(
                "a.bin", output, max_concurrency=1, checkpoint=self.checkpoint
            )
        service.failures.clear()
        self.assertEqual(output.getvalue(), data[:5000])
        with self.subTest("a stream elsewhere is refused"):
            with self.assertRaisesRegex(
                InvalidParameterError, "recorded 5000 bytes"
            ):
                self.client(service).file.download_stream(
                    "a.bin", io.BytesIO(), checkpoint=self.checkpoint
                )
        before = len(service.ranges())
        self.client(service).file.download_stream(
            "a.bin", output, checkpoint=self.checkpoint
        )
        self.assertEqual(output.getvalue(), data)
        self.assertTrue(
            all(
                int(r[6:].split("-")[0]) >= 5000
                for r in service.ranges()[before:]
            )
        )
        self.assertFalse(self.checkpoint.exists())

    def test_a_stream_download_of_a_file_changed_since_the_checkpoint_fails(
        self,
    ):
        service = DownloadService(self, content(9500))
        service.fail(5000, status=500, times=99)
        output = io.BytesIO()
        with self.assertRaises(APIError):
            self.client(service, max_network_retries=0).file.download_stream(
                "a.bin", output, max_concurrency=1, checkpoint=self.checkpoint
            )
        service.failures.clear()
        service.content = content(9500, seed=2)
        with self.assertRaisesRegex(
            InvalidRequestError, "changed while it was being downloaded"
        ):
            self.client(service).file.download_stream(
                "a.bin", output, checkpoint=self.checkpoint
            )
        self.assertEqual(len(output.getvalue()), 5000)

    def test_a_download_checkpoint_is_for_one_destination(self):
        service = DownloadService(self, content(9500))
        self.failed_first(service, self.scratch / "a.bin")
        with self.assertRaisesRegex(
            InvalidParameterError, "destination differs"
        ):
            self.client(service).file.download_file(
                "a.bin", self.scratch / "b.bin", checkpoint=self.checkpoint
            )
        with self.assertRaisesRegex(InvalidParameterError, "file of its own"):
            self.client(service).file.download_file(
                "a.bin", self.checkpoint, checkpoint=self.checkpoint
            )


@unittest.skipIf(
    sys.platform == "win32", "Windows gives no owners or permissions to check"
)
class TestCheckpointTrust(ResumeTestCase):
    """A checkpoint decides which bytes are not fetched again, so it is used
    only from where no other user can have written it."""

    def interrupted(self, service, target):
        """Download one range at a time with the range at 5000 failing for
        good: the preallocated temporary file holds 0-4999 and zeros."""
        service.fail(5000, status=500, times=99)
        with self.assertRaises(APIError):
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", target, max_concurrency=1, checkpoint=self.checkpoint
            )
        service.failures.clear()

    def forge(self, change):
        """What a writer who knows the genuine checkpoint could save: a
        changed state, with its digest computed again."""
        document = self.saved()
        change(document["state"])
        body = {
            name: document[name]
            for name in ("files_sdk_checkpoint", "kind", "key", "state")
        }
        document["sha256"] = digest(body)
        self.checkpoint.write_text(json.dumps(document))

    def untouched(self, target):
        """Everything a refused checkpoint must leave as it was."""
        return (
            self.stages(),
            {
                name: (self.scratch / name).read_bytes()
                for name in self.stage_files()
            },
            target.read_bytes() if target.exists() else None,
            self.checkpoint.read_bytes(),
        )

    def test_a_download_checkpoint_other_users_could_write_is_refused_before_anything_changes(
        self,
    ):
        data = content(9500)
        service = DownloadService(self, data)
        target = self.scratch / "a.bin"
        target.write_bytes(b"previous")
        self.interrupted(service, target)
        # It claims every byte arrived: the temporary file already has the
        # full size, and its version is genuine, so neither would tell.
        self.forge(lambda state: state.update(written=[[0, 9499]]))
        sent = (len(service.negotiations), len(service.ranges()))
        writable = (
            ("the checkpoint", self.checkpoint, 0o622, 0o600),
            ("its folder", self.scratch, 0o777, 0o700),
        )
        for label, path, shared, private in writable:
            with self.subTest(label):
                before = self.untouched(target)
                os.chmod(path, shared)
                try:
                    with self.assertRaisesRegex(
                        InvalidRequestError, "can be changed by other users"
                    ):
                        self.client(service).file.download_file(
                            "a.bin", target, checkpoint=self.checkpoint
                        )
                finally:
                    os.chmod(path, private)
                self.assertEqual(self.untouched(target), before)
                self.assertEqual(
                    (len(service.negotiations), len(service.ranges())), sent
                )

    def test_a_checkpoint_or_lock_file_that_is_a_link_or_that_others_can_write_is_refused(
        self,
    ):
        service = DownloadService(self, content(9500))
        target = self.scratch / "a.bin"
        self.interrupted(service, target)
        sent = len(service.negotiations)
        elsewhere = self.scratch / "elsewhere.checkpoint"
        os.replace(self.checkpoint, elsewhere)
        self.checkpoint.symlink_to(elsewhere)
        with self.assertRaisesRegex(
            InvalidRequestError, "its file is a symbolic link"
        ):
            self.client(service).file.download_file(
                "a.bin", target, checkpoint=self.checkpoint
            )
        self.checkpoint.unlink()
        os.replace(elsewhere, self.checkpoint)
        lock = Path(str(self.checkpoint) + ".lock")
        os.chmod(lock, 0o666)
        with self.assertRaisesRegex(
            InvalidRequestError, "its lock file can be changed by other users"
        ):
            self.client(service).file.download_file(
                "a.bin", target, checkpoint=self.checkpoint
            )
        self.assertEqual(len(service.negotiations), sent)

    def test_a_private_checkpoint_resumes_in_another_process_with_the_exact_bytes(
        self,
    ):
        data = content(9500)
        service = DownloadService(self, data)
        service.fail(5000, status=500, times=99)
        target = self.scratch / "a.bin"
        script = (
            "import sys, files_sdk, files_sdk.download\n"
            "files_sdk.download.DEFAULT_RANGE_SIZE = 1000\n"
            "client = files_sdk.Client(api_key='key', base_url=sys.argv[1], max_network_retries=0)\n"
            "client.file.download_file('a.bin', sys.argv[2], max_concurrency=1, checkpoint=sys.argv[3])\n"
        )
        child = subprocess.run(
            [
                sys.executable,
                "-c",
                script,
                service.url,
                str(target),
                str(self.checkpoint),
            ],
            cwd=os.getcwd(),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60,
        )
        self.assertNotEqual(child.returncode, 0)
        self.assertEqual(self.saved()["state"]["written"], [[0, 4999]])
        service.failures.clear()
        before = len(service.ranges())
        # Through a link of the user's own to the checkpoint's folder.
        (self.scratch / "via").symlink_to(self.scratch)

        self.client(service).file.download_file(
            "a.bin",
            target,
            checkpoint=self.scratch / "via" / self.checkpoint.name,
        )

        self.assertEqual(target.read_bytes(), data)
        self.assertEqual(
            sorted(service.ranges()[before:]),
            sorted(
                "bytes={}-{}".format(s, min(s + RANGE, 9500) - 1)
                for s in range(5000, 9500, RANGE)
            ),
        )
        self.assertFalse(self.checkpoint.exists())
        self.assertEqual(self.stages(), [])

    def test_a_new_file_gets_the_resuming_process_permissions_never_the_checkpoints(
        self,
    ):
        # A new destination gets what a new file of the resuming process
        # gets; one that exists keeps its own permissions.
        for existing in (None, 0o640):
            with self.subTest(existing=existing):
                data = content(9500)
                service = DownloadService(self, data)
                target = self.scratch / "a{}.bin".format(existing)
                if existing is not None:
                    target.write_bytes(b"previous")
                    os.chmod(target, existing)
                umask = os.umask(0o022)
                try:
                    self.interrupted(service, target)
                    self.forge(lambda state: state["stage"].update(mode=0o666))
                    os.umask(0o077)
                    self.client(service).file.download_file(
                        "a.bin", target, checkpoint=self.checkpoint
                    )
                finally:
                    os.umask(umask)
                self.assertEqual(target.read_bytes(), data)
                self.assertEqual(
                    stat.S_IMODE(target.stat().st_mode),
                    0o600 if existing is None else existing,
                )

    def test_a_checkpoint_replaced_while_the_download_runs_is_left_alone(self):
        data = content(9500)
        service = DownloadService(self, data)
        service.fail(5000, status=500, times=99)
        target = self.scratch / "a.bin"
        replacement = b'{"replaced": true}'

        def replace(range_header):
            if range_header.startswith("bytes=5000-"):
                temporary = self.scratch / "replacement"
                temporary.write_bytes(replacement)
                os.replace(temporary, self.checkpoint)

        service.on_request = replace
        with self.assertRaises(APIError) as caught:
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", target, max_concurrency=1, checkpoint=self.checkpoint
            )
        # The download's own error, with why its checkpoint was not saved.
        self.assertEqual(caught.exception.http_status, 500)
        self.assertIn(
            "was replaced since this transfer read or wrote it",
            "\n".join(caught.exception.__notes__),
        )
        self.assertEqual(self.checkpoint.read_bytes(), replacement)
        self.assertFalse(target.exists())
        self.assertEqual(self.stages(), [])


def acl(*arguments):
    """Change or remove (-N) a macOS access control list with its own tool."""
    subprocess.run(["/bin/chmod", *arguments], check=True, timeout=10)


def has_acl(path):
    return (
        len(
            subprocess.run(
                ["/bin/ls", "-lde", str(path)],
                check=True,
                capture_output=True,
                text=True,
                timeout=10,
            ).stdout.splitlines()
        )
        > 1
    )


def icacls(path, grant):
    """Grant a Windows access control entry with its own tool."""
    subprocess.run(
        ["icacls", str(path), "/grant", grant],
        check=True,
        capture_output=True,
        timeout=10,
    )


@unittest.skipUnless(
    sys.platform == "darwin", "macOS extended access control lists"
)
class TestCheckpointAccessControlLists(ResumeTestCase):
    """An access control list can let others change a file whatever its
    permissions say, so it counts as much as they do."""

    interrupted = TestCheckpointTrust.interrupted
    forge = TestCheckpointTrust.forge
    untouched = TestCheckpointTrust.untouched

    def setUp(self):
        import pwd

        super().setUp()
        self.addCleanup(
            lambda: [
                acl("-N", str(path))
                for path in (self.scratch, *self.scratch.iterdir())
                if not path.is_symlink()
            ]
        )
        self.user = pwd.getpwuid(os.geteuid()).pw_name

    def test_a_checkpoint_folder_or_lock_file_whose_list_lets_others_change_it_is_refused(
        self,
    ):
        data = content(9500)
        service = DownloadService(self, data)
        target = self.scratch / "a.bin"
        self.interrupted(service, target)
        self.forge(lambda state: state.update(written=[[0, 9499]]))
        lock = Path(str(self.checkpoint) + ".lock")
        sent = (len(service.negotiations), len(service.ranges()))
        grants = (
            ("the checkpoint", self.checkpoint, "everyone allow read,write"),
            (
                "its folder",
                self.scratch,
                "everyone allow add_file,delete_child",
            ),
            ("its lock file", lock, "everyone allow write"),
        )
        for label, path, grant in grants:
            with self.subTest(label):
                before = self.untouched(target)
                acl("+a", grant, str(path))
                try:
                    with self.assertRaisesRegex(
                        InvalidRequestError,
                        "access control list entry that lets another user or group change it",
                    ):
                        self.client(service).file.download_file(
                            "a.bin", target, checkpoint=self.checkpoint
                        )
                finally:
                    acl("-N", str(path))
                self.assertEqual(self.untouched(target), before)
                self.assertEqual(
                    (len(service.negotiations), len(service.ranges())), sent
                )

    def test_a_list_that_gives_no_one_else_a_way_in_still_resumes_with_the_exact_bytes(
        self,
    ):
        data = content(9500)
        service = DownloadService(self, data)
        target = self.scratch / "a.bin"
        self.interrupted(service, target)
        before = len(service.ranges())
        # Denying, granting this user, and grants only for items made later
        # let no one else change what is there.
        acl("+a", "everyone deny delete", str(self.scratch))
        acl(
            "+a",
            "everyone allow write,delete,file_inherit,only_inherit",
            str(self.scratch),
        )
        acl("+a", "everyone deny write", str(self.checkpoint))
        acl(
            "+a", "user:{} allow write".format(self.user), str(self.checkpoint)
        )

        self.client(service).file.download_file(
            "a.bin", target, checkpoint=self.checkpoint
        )

        self.assertEqual(target.read_bytes(), data)
        self.assertEqual(
            sorted(service.ranges()[before:]),
            sorted(
                "bytes={}-{}".format(s, min(s + RANGE, 9500) - 1)
                for s in range(5000, 9500, RANGE)
            ),
        )
        self.assertFalse(self.checkpoint.exists())

    def test_a_new_checkpoint_and_lock_file_are_private_from_the_moment_they_exist(
        self,
    ):
        import fcntl

        data = content(9500)
        service = DownloadService(self, data)
        target = self.scratch / "a.bin"
        # Others may pass through the folder, and every file made in it from
        # now on would let everyone read and write it.
        os.chmod(self.scratch, 0o755)
        acl(
            "+a",
            "everyone allow read,write,file_inherit,only_inherit",
            str(self.scratch),
        )
        probe = self.scratch / "probe"
        probe.write_bytes(b"")
        self.assertTrue(has_acl(probe))
        probe.unlink()
        # What each new checkpoint or lock file was the moment it was made, and
        # its folder then: a descriptor opened at that moment would outlast
        # any later change.
        real_open, created = os.open, []

        def observed(path, flags, mode=0o777, *, dir_fd=None):
            handle = real_open(path, flags, mode, dir_fd=dir_fd)
            if flags & os.O_CREAT:
                made = (
                    fcntl.fcntl(handle, fcntl.F_GETPATH, bytes(1024))
                    .rstrip(b"\0")
                    .decode()
                )
                name = os.path.basename(made)
                if name in ("checkpoint", "lock") or name.endswith(
                    (".tmp", ".lock")
                ):
                    folder = os.path.dirname(made)
                    created.append(
                        (
                            name,
                            has_acl(made),
                            stat.S_IMODE(os.stat(folder).st_mode),
                            has_acl(folder),
                        )
                    )
            return handle

        with mock.patch("os.open", observed):
            self.interrupted(service, target)
            lock = Path(str(self.checkpoint) + ".lock")
            self.assertEqual(
                (has_acl(self.checkpoint), has_acl(lock)), (False, False)
            )
            self.client(service).file.download_file(
                "a.bin", target, checkpoint=self.checkpoint
            )

        self.assertEqual(target.read_bytes(), data)
        # Every one had no access control list, in an owner-only folder without one.
        self.assertEqual(
            {
                (acl_then, folder_mode, folder_acl)
                for _name, acl_then, folder_mode, folder_acl in created
            },
            {(False, 0o700, False)},
        )
        self.assertTrue(
            {"lock", "checkpoint"} <= {name for name, *_ in created}
        )
        self.assertEqual(
            [
                name
                for name in os.listdir(self.scratch)
                if name.endswith(".stage")
            ],
            [],
        )

    def test_a_save_that_cannot_make_its_staging_folder_keeps_the_last_checkpoint(
        self,
    ):
        data = content(9500)
        service = DownloadService(self, data)
        service.fail(5000, status=500, times=99)
        target = self.scratch / "a.bin"
        # Nothing more can be made in the folder once the failing range is asked for.
        service.on_request = lambda range_header: (
            os.chmod(self.scratch, 0o500)
            if range_header.startswith("bytes=5000-")
            else None
        )
        self.addCleanup(os.chmod, self.scratch, 0o700)
        with self.assertRaises(APIError) as caught:
            self.client(service, max_network_retries=0).file.download_file(
                "a.bin", target, max_concurrency=1, checkpoint=self.checkpoint
            )
        os.chmod(self.scratch, 0o700)
        self.assertEqual(caught.exception.http_status, 500)
        self.assertIn(
            "could not be saved", "\n".join(caught.exception.__notes__)
        )
        # The checkpoint saved while the download ran is still there, whole.
        kept = self.saved()
        self.assertTrue(kept["state"]["written"])
        self.assertEqual(
            [
                name
                for name in os.listdir(self.scratch)
                if name.endswith(".stage")
            ],
            [],
        )
        service.failures.clear()
        service.on_request = None
        self.client(service).file.download_file(
            "a.bin", target, checkpoint=self.checkpoint
        )
        self.assertEqual(target.read_bytes(), data)


def sid(text):
    """A binary SID from its S-1-... form."""
    parts = [int(part) for part in text.split("-")[1:]]
    revision, authority, subs = parts[0], parts[1], parts[2:]
    return (
        bytes([revision, len(subs)])
        + authority.to_bytes(6, "big")
        + b"".join(sub.to_bytes(4, "little") for sub in subs)
    )


def descriptor(owner, entries, dacl=True):
    """A self-relative Windows security descriptor, as GetFileSecurityW
    returns one: an owner and a list of (type, flags, mask, SID) entries."""
    aces = b""
    for kind, flags, mask, who in entries:
        body = mask.to_bytes(4, "little") + sid(who)
        aces += (
            bytes([kind, flags]) + (4 + len(body)).to_bytes(2, "little") + body
        )
    owner_bytes = sid(owner)
    acl_bytes = (
        bytes([2, 0])
        + (8 + len(aces)).to_bytes(2, "little")
        + len(entries).to_bytes(2, "little")
        + b"\0\0"
        + aces
    )
    owner_at, dacl_at = 20, 20 + len(owner_bytes)
    control = 0x8000 | (0x0004 if dacl else 0)
    header = (
        bytes([1, 0])
        + control.to_bytes(2, "little")
        + owner_at.to_bytes(4, "little")
        + bytes(8)
    )
    header += (dacl_at if dacl else 0).to_bytes(4, "little")
    return header + owner_bytes + (acl_bytes if dacl else b"")


class TestWindowsCheckpointAccess(unittest.TestCase):
    """What Windows owners and access control lists let a checkpoint be
    trusted with. Windows itself is not run here: these descriptors are
    built as GetFileSecurityW and GetKernelObjectSecurity return them."""

    USER = "S-1-5-21-1004336348-1177238915-682003330-1001"
    OTHER = "S-1-5-21-1004336348-1177238915-682003330-1002"
    FULL = 0x1F01FF
    MODIFY = 0x1301BF
    READ = 0x1200A9
    PRIVATE = [
        (0, 0x10, FULL, "S-1-5-18"),
        (0, 0x10, FULL, "S-1-5-32-544"),
        (0, 0x10, FULL, USER),
    ]

    def folder(self, data):
        from files_sdk import access

        return access._windows_problem(
            data,
            self.USER,
            "C:\\work",
            access._FOLDER_WRITES,
            access._FOLDER_OWNERS,
        )

    def file(self, data, new=False):
        from files_sdk import access

        rights = access._NEW_FILE_ACCESS if new else access._FILE_WRITES
        return access._windows_problem(
            data, self.USER, "its file", rights, access._FILE_OWNERS
        )

    def test_a_private_profile_folder_and_file_are_trusted(self):
        self.assertIsNone(self.folder(descriptor(self.USER, self.PRIVATE)))
        self.assertIsNone(
            self.file(descriptor(self.USER, self.PRIVATE), new=True)
        )
        # A drive's root: others may make folders there and read, and inherit
        # Modify only into what they make, as C:\\ allows by default.
        root = [
            (0, 0, self.FULL, "S-1-5-32-544"),
            (0, 0, self.FULL, "S-1-5-18"),
            (0, 0x03, self.READ, "S-1-5-32-545"),
            (0, 0x0B, self.MODIFY, "S-1-5-11"),
            (0, 0, 0x0004, "S-1-5-11"),
            (0, 0x0B, 0x10000000, "S-1-3-0"),
        ]
        self.assertIsNone(
            self.folder(
                descriptor(
                    "S-1-5-80-956008885-3418522649-1831038044-1853292631-2271478464",
                    root,
                )
            )
        )

    def test_a_folder_others_can_change_or_empty_is_not_trusted(self):
        for mask in (
            self.MODIFY,
            0x0040,
            0x10000,
            0x40000,
            0x80000,
            0x10000000,
            0x40000000,
        ):
            with self.subTest(mask=hex(mask)):
                problem = self.folder(
                    descriptor(
                        self.USER, self.PRIVATE + [(0, 0x10, mask, "S-1-5-11")]
                    )
                )
                self.assertIn("lets S-1-5-11 change it", problem)
        # What a folder made directly in C:\\ inherits from it.
        self.assertIsNotNone(
            self.folder(
                descriptor(
                    self.USER,
                    self.PRIVATE + [(0, 0x10, self.MODIFY, "S-1-5-11")],
                )
            )
        )

    def test_a_file_others_can_write_or_a_new_one_they_can_read_is_not_trusted(
        self,
    ):
        self.assertIn(
            "lets S-1-1-0 change it",
            self.file(
                descriptor(
                    self.USER, self.PRIVATE + [(0, 0, 0x0002, "S-1-1-0")]
                )
            ),
        )
        readable = descriptor(
            self.USER, self.PRIVATE + [(0, 0x10, self.READ, "S-1-5-32-545")]
        )
        self.assertIsNone(self.file(readable))
        self.assertIsNotNone(self.file(readable, new=True))
        # Denying takes nothing away from this user; it is not a grant.
        self.assertIsNone(
            self.file(
                descriptor(
                    self.USER, self.PRIVATE + [(1, 0, self.FULL, "S-1-1-0")]
                )
            )
        )

    def test_a_folder_that_passes_new_files_access_for_others_is_refused(self):
        from files_sdk import access

        def passes(entries):
            return access._windows_inheritance_problem(
                descriptor(self.USER, entries), self.USER, "C:\\work"
            )

        # Object-inherit (0x01) entries reach every new file; CREATOR OWNER becomes this user.
        self.assertIsNone(
            passes(
                [
                    (0, 0x03, self.FULL, "S-1-5-18"),
                    (0, 0x03, self.FULL, self.USER),
                    (0, 0x0B, self.FULL, "S-1-3-0"),
                ]
            )
        )
        self.assertIn(
            "gives S-1-5-32-545 access",
            passes(self.PRIVATE + [(0, 0x0B, self.READ, "S-1-5-32-545")]),
        )
        # Folders only (container-inherit, 0x02) do not reach files.
        self.assertIsNone(
            passes(self.PRIVATE + [(0, 0x02, self.READ, "S-1-5-32-545")])
        )
        self.assertIn(
            "no access control list",
            passes([])
            or access._windows_inheritance_problem(
                descriptor(self.USER, [], dacl=False), self.USER, "C:\\work"
            ),
        )

    def test_an_owner_list_or_entry_that_cannot_be_trusted_is_refused(self):
        self.assertIn(
            "belongs to another user",
            self.file(descriptor(self.OTHER, self.PRIVATE)),
        )
        self.assertIsNone(self.file(descriptor("S-1-5-32-544", self.PRIVATE)))
        self.assertIn(
            "no access control list",
            self.folder(descriptor(self.USER, [], dacl=False)),
        )
        self.assertIsNone(self.folder(descriptor(self.USER, [])))
        self.assertIn(
            "cannot read",
            self.file(
                descriptor(
                    self.USER, self.PRIVATE + [(0x05, 0, 0x0002, "S-1-1-0")]
                )
            ),
        )
        self.assertIn(
            "could not be read",
            self.file(descriptor(self.USER, self.PRIVATE)[:-7]),
        )


if __name__ == "__main__":
    unittest.main()

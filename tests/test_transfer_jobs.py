import os
import random
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest import mock

import files_sdk
import requests
from files_sdk.error import (
    InvalidParameterError,
    InvalidRequestError,
    OperationCancelledError,
    TransferPausedError,
)
from tests.download_fixtures import TreeService, token_of
from tests.upload_fixtures import UploadService


def content(size, seed=1):
    return random.Random(seed).randbytes(size)


class JobTestCase(unittest.TestCase):
    def setUp(self):
        scratch = tempfile.TemporaryDirectory()
        self.addCleanup(scratch.cleanup)
        self.scratch = Path(scratch.name)
        self.checkpoint = self.scratch / "job.checkpoint"

    def client(self, service, **settings):
        client = files_sdk.Client(
            api_key="key",
            base_url=service.url,
            initial_network_retry_delay=0,
            **settings,
        )
        self.addCleanup(client.close)
        return client

    def tree(self, files, folders=()):
        root = self.scratch / "source"
        root.mkdir()
        for name, data in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        for name in folders:
            (root / name).mkdir(parents=True, exist_ok=True)
        return root


class TestUploadDirectory(JobTestCase):
    def test_files_and_empty_folders_upload_with_their_relative_paths(self):
        files = {
            "a.txt": b"alpha",
            "sub/b.bin": content(2500),
            "sub/deeper/c.txt": b"gamma",
        }
        root = self.tree(files, folders=["empty/inner"])
        if sys.platform != "win32":
            (root / "link.txt").symlink_to(root / "a.txt")
        service = UploadService(self, part_size=1000)
        reports = []

        result = self.client(service).file.upload_directory(
            root, "backup", progress=reports.append, max_files=2
        )

        for name, data in files.items():
            self.assertEqual(service.completed("backup/" + name), data)
        self.assertEqual(service.folders, ["backup/empty/inner"])
        self.assertTrue(
            all(
                begin.get("mkdir_parents")
                for begin in service.begins
                if "ref" not in begin
            )
        )
        self.assertTrue(result.ok)
        self.assertEqual(
            sorted(o.remote_path for o in result.completed),
            sorted(["backup/" + n for n in files] + ["backup/empty/inner"]),
        )
        if sys.platform != "win32":
            [skipped] = result.skipped
            self.assertEqual(
                (skipped.remote_path, skipped.reason),
                ("backup/link.txt", "symbolic link"),
            )
        last = reports[-1]
        self.assertEqual(
            (last.files_completed, last.files_found, last.scan_complete),
            (3, 3, True),
        )
        self.assertEqual(
            last.bytes_committed, sum(len(d) for d in files.values())
        )

    def test_one_failing_file_does_not_stop_the_others(self):
        root = self.tree(
            {"good1.txt": b"1", "bad.txt": b"2", "good2.txt": b"3"}
        )
        service = UploadService(self, part_size=1000)
        service.refuse_paths = {"up/bad.txt"}
        result = self.client(service).file.upload_directory(root, "up")
        self.assertFalse(result.ok)
        [failed] = result.failed
        self.assertEqual(failed.remote_path, "up/bad.txt")
        self.assertIsInstance(failed.error, files_sdk.error.Error)
        self.assertEqual(
            sorted(service.completed_paths()), ["up/good1.txt", "up/good2.txt"]
        )

    def test_files_at_once_stay_within_max_files_and_the_shared_limiter(self):
        root = self.tree(
            {"f{}.bin".format(i): content(3000, seed=i) for i in range(8)}
        )
        service = UploadService(self, part_size=1000)
        service.on_put = lambda number: time.sleep(0.02)
        limiter = files_sdk.TransferLimiter(max_parts=3)
        seen = []
        original = service.on_put
        service.on_put = lambda number: (
            seen.append(limiter.parts_in_use),
            original(number),
        )
        result = self.client(
            service, transfer_limiter=limiter
        ).file.upload_directory(root, "", max_files=3, max_concurrency=4)
        self.assertTrue(result.ok)
        self.assertLessEqual(max(seen), 3)
        self.assertLessEqual(service.max_active, 3)
        self.assertEqual((limiter.parts_in_use, limiter.bytes_in_use), (0, 0))

    def test_a_job_s_files_share_one_request_budget(self):
        # Four files at once, but never more parts at once than the target
        # they share, rather than that target for each file: also when
        # Files.com asks every other upload to send its parts one at a time,
        # and when the cap is one part at a time for the whole job.
        files = {"f{}.bin".format(i): content(800, seed=i) for i in range(4)}
        root = self.tree(files)
        tuning = files_sdk.UploadTuning(
            initial_concurrency=2, grow_every=1000, throughput_window=0
        )
        for name, serial, max_concurrency, most in (
            ("parallel", False, 8, 2),
            ("mixed", True, 8, 2),
            ("cap one", False, 1, 1),
        ):
            with self.subTest(name):
                service = UploadService(self, part_size=100)
                service.on_put = lambda number: time.sleep(0.05)
                if serial:
                    original = service.describe

                    def describe(ref, number, original=original):
                        record = original(ref, number)
                        record["parallel_parts"] = (
                            int(ref.rsplit("-", 1)[1]) % 2 == 0
                        )
                        return record

                    service.describe = describe
                limiter = files_sdk.TransferLimiter()
                client = self.client(service, transfer_limiter=limiter)
                result = client.file.upload_directory(
                    root,
                    name,
                    max_files=4,
                    max_concurrency=max_concurrency,
                    tuning=tuning,
                )
                self.assertTrue(result.ok)
                self.assertEqual(most, service.max_active)
                for file_name, data in files.items():
                    self.assertEqual(
                        data,
                        service.completed("{}/{}".format(name, file_name)),
                    )
                self.assertEqual(
                    (0, 0), (limiter.parts_in_use, limiter.bytes_in_use)
                )

    def test_later_files_of_a_job_inherit_what_it_learned_and_another_job_starts_afresh(
        self,
    ):
        # The first file's part 1 is answered 503, which halves the job's
        # target; the next files start at the halved target. Another job
        # through the same client and limiter starts at its own.
        root = self.tree(
            {"f{}.bin".format(i): content(400, seed=i) for i in range(3)}
        )
        service = UploadService(self, part_size=100)
        service.fail(1, status=503)
        observed = []
        tuning = files_sdk.UploadTuning(
            initial_concurrency=4,
            backpressure_pause=0,
            grow_every=1000,
            throughput_window=0,
            observer=observed.append,
        )
        client = self.client(service)
        self.assertTrue(
            client.file.upload_directory(
                root, "first", max_files=1, max_concurrency=4, tuning=tuning
            ).ok
        )
        self.assertEqual(
            [4, 2, 2],
            [o.target_concurrency for o in observed if o.kind == "start"],
        )
        observed.clear()
        self.assertTrue(
            client.file.upload_directory(
                root, "second", max_files=1, max_concurrency=4, tuning=tuning
            ).ok
        )
        self.assertEqual(
            [4, 4, 4],
            [o.target_concurrency for o in observed if o.kind == "start"],
        )

    def test_without_max_files_an_s3_job_prepares_enough_files_to_feed_its_target(
        self,
    ):
        # Before any of its uploads has a controller, the job takes the
        # target as four, so six files at first: with their first requests
        # held, six have begun and no more. Once the target of 150 is known,
        # one-part files cannot fill it six at a time: the job prepares up to
        # 128 at once, here with every answer held until 128 parts are in
        # progress, and no more. With max_files, it keeps to it.
        root = self.tree(
            {"f{:03}.txt".format(i): b"x" * 10 for i in range(130)}
        )
        tuning = files_sdk.UploadTuning(
            startup=files_sdk.UploadStartup.AGGRESSIVE
        )
        first = UploadService(
            self, part_size=1000, grant={"upload_target_class": "s3"}
        )
        begun, six, release = [], threading.Event(), threading.Event()
        self.addCleanup(release.set)
        lock = threading.Lock()
        send = requests.Session.send

        def hold_first_requests(session, request, **kwargs):
            if (
                "/file_actions/begin_upload/" in request.url
                and b'"ref"' not in (request.body or b"")
            ):
                with lock:
                    begun.append(request.url)
                    if len(begun) >= 6:
                        six.set()
                release.wait(10)
            return send(session, request, **kwargs)

        results = []
        client = self.client(first)
        with mock.patch.object(requests.Session, "send", hold_first_requests):
            job = threading.Thread(
                target=lambda: results.append(
                    client.file.upload_directory(root, "first", tuning=tuning)
                )
            )
            job.start()
            self.assertTrue(six.wait(10))
            time.sleep(0.3)  # Several of the job's 100 ms rechecks.
            at_first = len(begun)
            release.set()
            job.join(60)
        self.assertEqual(6, at_first)
        self.assertTrue(results[0].ok)
        service = UploadService(
            self, part_size=1000, grant={"upload_target_class": "s3"}
        )
        crowd = threading.Event()

        def wait_for_the_crowd(number):
            if service.active >= 128:
                crowd.set()
            crowd.wait(10)

        service.on_put = wait_for_the_crowd
        self.assertTrue(
            self.client(service)
            .file.upload_directory(root, "second", tuning=tuning)
            .ok
        )
        self.assertTrue(crowd.is_set())
        self.assertEqual(128, service.max_active)
        capped = UploadService(
            self, part_size=1000, grant={"upload_target_class": "s3"}
        )
        capped.on_put = lambda number: time.sleep(0.005)
        self.assertTrue(
            self.client(capped)
            .file.upload_directory(root, "up", max_files=2, tuning=tuning)
            .ok
        )
        self.assertLessEqual(capped.max_active, 2)

    def test_a_file_renewing_its_url_holds_no_place_another_file_could_use(
        self,
    ):
        # Two one-part files share a cap of one part at a time, and each
        # part's first URL has already expired. The first renewal to arrive
        # is held until a part arrives at storage: the other file sends its
        # part meanwhile, because the renewing file holds no place.
        files = {"a.bin": content(300, seed=1), "b.bin": content(300, seed=2)}
        root = self.tree(files)
        service = UploadService(self, part_size=1000)
        service.expire_first()
        arrived = threading.Event()
        service.on_put = lambda number: arrived.set()
        held = []
        lock = threading.Lock()
        send = requests.Session.send

        def hold_the_first_renewal(session, request, **kwargs):
            first = False
            if "/file_actions/begin_upload/" in request.url and b'"ref"' in (
                request.body or b""
            ):
                with lock:
                    first = not held
                    if first:
                        held.append(None)
            if first:
                held[0] = arrived.wait(10)
            return send(session, request, **kwargs)

        observed = []
        limiter = files_sdk.TransferLimiter()
        client = self.client(service, transfer_limiter=limiter)
        tuning = files_sdk.UploadTuning(observer=observed.append)
        with mock.patch.object(
            requests.Session, "send", hold_the_first_renewal
        ):
            result = client.file.upload_directory(
                root, "up", max_files=2, max_concurrency=1, tuning=tuning
            )
        self.assertTrue(result.ok)
        self.assertEqual([True], held)
        for name, data in files.items():
            self.assertEqual(data, service.completed("up/" + name))
        self.assertEqual(0, observed[-1].attempts_in_progress)
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))

    def test_a_file_failing_its_source_check_teaches_the_job_nothing_from_its_stopped_parts(
        self,
    ):
        # The first file changes once its part 1 has arrived, while its parts
        # 2 to 4 are held at storage: reading its part 5 fails it, and its
        # held parts are stopped. Stopped attempts are not failures: the next
        # files start at the job's unchanged target of four, and no failure
        # is learned.
        files = {
            "a.bin": content(600, seed=1),
            "b.bin": content(200, seed=2),
            "c.bin": content(200, seed=3),
        }
        root = self.tree(files)
        service = UploadService(self, part_size=100)
        for number in (2, 3, 4):
            service.hold(number)

        def on_put(number):
            if number == 1 and service.puts.count(1) == 1:
                (root / "a.bin").write_bytes(content(600, seed=9))
            elif number == 1:
                for held in (2, 3, 4):
                    service.release(held)

        service.on_put = on_put
        observed = []
        limiter = files_sdk.TransferLimiter()
        tuning = files_sdk.UploadTuning(
            initial_concurrency=4,
            grow_every=1000,
            throughput_window=0,
            observer=observed.append,
        )
        client = self.client(service, transfer_limiter=limiter)

        result = client.file.upload_directory(
            root, "up", max_files=1, max_concurrency=8, tuning=tuning
        )

        [failed] = result.failed
        self.assertTrue(failed.local_path.endswith("a.bin"))
        self.assertIsInstance(failed.error, InvalidRequestError)
        for name in ("b.bin", "c.bin"):
            self.assertEqual(files[name], service.completed("up/" + name))
        self.assertEqual(
            [4, 4, 4],
            [o.target_concurrency for o in observed if o.kind == "start"],
        )
        self.assertFalse(
            {o.decision for o in observed if o.kind == "decision"}
            & {"failure", "stale_failure"}
        )
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))

    def test_a_paused_job_resumes_skipping_files_completed_before(self):
        files = {"f{}.bin".format(i): content(2000, seed=i) for i in range(6)}
        root = self.tree(files)
        service = UploadService(self, part_size=1000)
        pause = files_sdk.PauseToken()
        service.on_put = lambda number: (
            time.sleep(0.02),
            len(service.finishes) >= 2 and pause.pause(),
        )
        with self.assertRaises(TransferPausedError) as caught:
            self.client(service).file.upload_directory(
                root,
                "p",
                max_files=2,
                checkpoint=self.checkpoint,
                pause_token=pause,
            )
        first = caught.exception.result
        self.assertTrue(first.completed)
        self.assertTrue(self.checkpoint.exists())
        finished_before = set(service.completed_paths())

        service.on_put = None
        result = self.client(service).file.upload_directory(
            root, "p", max_files=2, checkpoint=self.checkpoint
        )
        self.assertTrue(result.ok)
        for name, data in files.items():
            self.assertEqual(service.completed("p/" + name), data)
        resumed = [
            o.remote_path
            for o in result.completed
            if o.reason == "completed before"
        ]
        self.assertEqual(sorted(resumed), sorted(p for p in finished_before))
        # No file completed twice.
        self.assertEqual(
            len(service.completed_paths()), len(set(service.completed_paths()))
        )
        self.assertFalse(self.checkpoint.exists())

    def test_a_changed_file_is_uploaded_again_on_resuming(self):
        root = self.tree({"a.txt": b"one", "b.txt": b"two"})
        service = UploadService(self, part_size=1000)
        service.refuse_paths = {"b.txt"}
        result = self.client(service).file.upload_directory(
            root, "", checkpoint=self.checkpoint
        )
        self.assertEqual(len(result.failed), 1)
        self.assertTrue(self.checkpoint.exists())
        (root / "a.txt").write_bytes(b"ONE!")
        os.utime(root / "a.txt", ns=(1, 1))
        service.refuse_paths = set()
        result = self.client(service).file.upload_directory(
            root, "", checkpoint=self.checkpoint
        )
        self.assertTrue(result.ok)
        self.assertEqual(service.completed("a.txt"), b"ONE!")
        self.assertEqual(service.completed("b.txt"), b"two")

    def test_cancelling_stops_the_whole_job_with_the_result_so_far(self):
        root = self.tree(
            {"f{}.bin".format(i): content(2000, seed=i) for i in range(10)}
        )
        service = UploadService(self, part_size=500)
        token = files_sdk.CancellationToken()
        service.on_put = lambda number: (
            time.sleep(0.02),
            len(service.finishes) >= 2 and token.cancel(),
        )
        with self.assertRaises(OperationCancelledError) as caught:
            self.client(service).file.upload_directory(
                root, "", {"cancel_token": token}, max_files=2
            )
        result = caught.exception.result  # type: ignore[attr-defined]
        self.assertIsInstance(result, files_sdk.TransferResult)
        self.assertTrue(
            any(o.status == "cancelled" for o in result.outcomes)
            or len(result.completed) >= 2
        )
        self.assertLess(len(service.finishes), 10)

    def test_invalid_job_arguments_are_refused_before_any_request(self):
        root = self.tree({"a.txt": b"x"})
        service = UploadService(self, part_size=1000)
        client = self.client(service)
        for settings in (
            {"max_files": 0},
            {"max_files": 65},
            {"max_concurrency": 0},
            {"progress": 3},
        ):
            with self.subTest(settings):
                with self.assertRaises(InvalidParameterError):
                    client.file.upload_directory(root, "", **settings)
        with self.assertRaisesRegex(
            InvalidParameterError, "not a local directory"
        ):
            client.file.upload_directory(root / "a.txt", "")
        with self.assertRaisesRegex(
            InvalidParameterError, "inside the local directory"
        ):
            client.file.upload_directory(
                root, "", checkpoint=root / "state.json"
            )
        with self.assertRaisesRegex(
            InvalidParameterError, "needs a checkpoint"
        ):
            client.file.upload_directory(
                root, "", pause_token=files_sdk.PauseToken()
            )
        self.assertEqual(service.begins, [])

    def test_upload_files_uploads_each_pair(self):
        a, b = self.scratch / "a.bin", self.scratch / "b.bin"
        a.write_bytes(content(1500))
        b.write_bytes(b"small")
        service = UploadService(self, part_size=1000)
        result = self.client(service).file.upload_files(
            [
                (a, "x/a.bin"),
                (str(b), "y/b.bin"),
                (self.scratch / "missing", "z"),
            ]
        )
        self.assertEqual(service.completed("x/a.bin"), a.read_bytes())
        self.assertEqual(service.completed("y/b.bin"), b"small")
        [failed] = result.failed
        self.assertEqual(failed.remote_path, "z")
        self.assertIsInstance(failed.error, FileNotFoundError)

    def test_the_module_function_uses_the_module_settings(self):
        root = self.tree({"a.txt": b"x"})
        service = UploadService(self, part_size=1000)
        from unittest import mock

        with mock.patch.multiple(
            files_sdk, base_url=service.url, the_api_key="key"
        ):
            result = files_sdk.upload_directory(str(root), "m")
        self.assertTrue(result.ok)
        self.assertEqual(service.completed("m/a.txt"), b"x")


class TestDownloadDirectory(JobTestCase):
    FILES = {
        "docs/a.txt": b"alpha",
        "docs/sub/b.bin": content(3000),
        "docs/sub/deep/c.txt": b"gamma",
        "docs/d.txt": b"delta",
        "other/x.txt": b"not listed",
    }

    def test_a_remote_folder_is_mirrored_locally(self):
        service = TreeService(self, self.FILES, folders=["docs/empty"])
        target = self.scratch / "mirror"
        result = self.client(service).file.download_directory(
            "docs", target, max_files=3
        )
        self.assertTrue(result.ok)
        for name, data in self.FILES.items():
            if name.startswith("docs/"):
                self.assertEqual(
                    (target / name[len("docs/") :]).read_bytes(), data
                )
        self.assertTrue((target / "empty").is_dir())
        self.assertFalse((target / "x.txt").exists())
        # Listings are fetched a page at a time.
        self.assertIn(("docs", "2"), service.listed)
        self.assertEqual(
            [
                n
                for n in os.listdir(target)
                if n.endswith(".files_sdk-download")
            ],
            [],
        )

    def test_a_file_that_fails_does_not_stop_the_others(self):
        service = TreeService(self, self.FILES)
        service.fail_paths = {"docs/d.txt"}
        target = self.scratch / "mirror"
        result = self.client(
            service, max_network_retries=0
        ).file.download_directory("docs", target)
        [failed] = result.failed
        self.assertEqual(failed.remote_path, "docs/d.txt")
        self.assertEqual((target / "a.txt").read_bytes(), b"alpha")
        self.assertFalse((target / "d.txt").exists())

    def test_a_destination_that_cannot_be_opened_keeps_its_error_when_the_job_is_cancelled(
        self,
    ):
        # One file at a time, without a progress callback: blocked/a.txt
        # cannot be opened, as its local folder is a regular file; then the
        # caller cancels while later/b.txt's content is on its way.
        service = TreeService(
            self, {"docs/blocked/a.txt": b"alpha", "docs/later/b.txt": b"beta"}
        )
        target = self.scratch / "mirror"
        target.mkdir()
        (target / "blocked").write_bytes(b"a file, not a folder")
        token = files_sdk.CancellationToken()
        service.on_download = lambda path: token.cancel()
        with self.assertRaises(OperationCancelledError) as caught:
            self.client(service).file.download_directory(
                "docs", target, {"cancel_token": token}, max_files=1
            )
        self.assertEqual(service.downloads, ["docs/later/b.txt"])
        result = caught.exception.result  # type: ignore[attr-defined]
        blocked, later = result.outcomes
        self.assertEqual(
            (blocked.status, blocked.remote_path, blocked.local_path),
            (
                "failed",
                "docs/blocked/a.txt",
                str(target / "blocked" / "a.txt"),
            ),
        )
        self.assertIsInstance(blocked.error, NotADirectoryError)
        self.assertEqual(
            (later.status, later.remote_path, later.error),
            ("cancelled", "docs/later/b.txt", None),
        )
        self.assertEqual(
            (target / "blocked").read_bytes(), b"a file, not a folder"
        )
        self.assertFalse((target / "later" / "b.txt").exists())

    def test_a_destination_that_cannot_be_opened_as_the_job_is_cancelled_keeps_its_error(
        self,
    ):
        # The caller cancels just as blocked/a.txt's local folder, a regular
        # file, is opened: the job stops with the cancellation, and the file
        # it could not open keeps its own error.
        from unittest import mock

        from files_sdk import localfs

        service = TreeService(
            self, {"docs/blocked/a.txt": b"alpha", "docs/later/b.txt": b"beta"}
        )
        target = self.scratch / "mirror"
        target.mkdir()
        (target / "blocked").write_bytes(b"a file, not a folder")
        token = files_sdk.CancellationToken()
        child = localfs.Directory.child

        def cancelling_child(directory, name, create=False):
            if name == "blocked":
                token.cancel()
            return child(directory, name, create)

        with mock.patch.object(localfs.Directory, "child", cancelling_child):
            with self.assertRaises(OperationCancelledError) as caught:
                self.client(service).file.download_directory(
                    "docs", target, {"cancel_token": token}, max_files=1
                )
        self.assertTrue(token.cancelled)
        self.assertEqual(service.downloads, [])
        [blocked] = caught.exception.result.outcomes  # type: ignore[attr-defined]
        self.assertEqual(
            (blocked.status, blocked.remote_path),
            ("failed", "docs/blocked/a.txt"),
        )
        self.assertIsInstance(blocked.error, NotADirectoryError)

    def test_a_folder_that_cannot_be_listed_fails_alone(self):
        service = TreeService(self, self.FILES)
        service.refuse_listing = {"docs/sub"}
        result = self.client(service).file.download_directory(
            "docs", self.scratch / "mirror"
        )
        [failed] = result.failed
        self.assertEqual(
            (failed.kind, failed.remote_path), ("folder", "docs/sub")
        )
        self.assertEqual(
            sorted(o.remote_path for o in result.completed),
            ["docs/a.txt", "docs/d.txt"],
        )

    def test_a_missing_remote_folder_raises(self):
        service = TreeService(self, self.FILES)
        with self.assertRaises(files_sdk.error.NotFoundError):
            self.client(service).file.download_directory(
                "nope", self.scratch / "mirror"
            )

    @unittest.skipIf(sys.platform == "win32", "symbolic links")
    def test_a_local_link_leading_outside_the_directory_is_not_written_through(
        self,
    ):
        service = TreeService(self, self.FILES)
        target = self.scratch / "mirror"
        outside = self.scratch / "outside"
        outside.mkdir()
        target.mkdir()
        (target / "sub").symlink_to(outside, target_is_directory=True)
        result = self.client(service).file.download_directory("docs", target)
        failed = sorted(o.remote_path for o in result.failed)
        self.assertEqual(failed, ["docs/sub/b.bin", "docs/sub/deep/c.txt"])
        self.assertEqual(os.listdir(outside), [])

    @unittest.skipUnless(
        sys.platform in ("darwin", "win32"), "case-insensitive local names"
    )
    def test_two_remote_names_for_one_local_file_are_not_both_written(self):
        service = TreeService(
            self, {"c/Read.txt": b"upper", "c/read.txt": b"lower"}
        )
        result = self.client(service).file.download_directory(
            "c", self.scratch / "mirror"
        )
        self.assertEqual(len(result.completed), 1)
        [failed] = result.failed
        self.assertIn("Another remote file", str(failed.error))

    def test_a_paused_download_job_resumes(self):
        files = {
            "p/f{}.bin".format(i): content(3000, seed=i) for i in range(6)
        }
        service = TreeService(self, files, page_size=10)
        service.delay = 0.02
        pause = files_sdk.PauseToken()
        target = self.scratch / "mirror"
        service.on_download = lambda path: (
            pause.pause() if len(service.downloads) == 3 else None
        )
        with self.assertRaises(TransferPausedError) as caught:
            self.client(service).file.download_directory(
                "p",
                target,
                max_files=2,
                checkpoint=self.checkpoint,
                pause_token=pause,
            )
        self.assertTrue(self.checkpoint.exists())
        self.assertTrue(caught.exception.result.completed)
        self.assertLess(len(caught.exception.result.completed), 6)
        service.on_download = None
        before = len(service.downloads)
        result = self.client(service).file.download_directory(
            "p", target, max_files=2, checkpoint=self.checkpoint
        )
        self.assertTrue(result.ok)
        for name, data in files.items():
            self.assertEqual((target / name[2:]).read_bytes(), data)
        completed_before = [
            o for o in result.completed if o.reason == "completed before"
        ]
        self.assertLessEqual(
            len(service.downloads) - before, 6 - len(completed_before)
        )
        self.assertFalse(self.checkpoint.exists())

    def test_a_download_job_s_adaptive_files_share_one_request_budget(self):
        # Four files at once, each one range that takes a while. Adaptive
        # downloads share the job's target, so never more ranges at once
        # than it, rather than that target for each file; downloads that do
        # not adapt keep their own.
        files = {
            "many/f{}.bin".format(i): content(800, seed=i) for i in range(6)
        }
        adaptive = files_sdk.UploadTuning(
            initial_concurrency=2, grow_every=1000, throughput_window=0
        )
        static = files_sdk.UploadTuning(adaptive=False)
        for name, tuning, max_concurrency, most in (
            ("adaptive", adaptive, 8, 2),
            ("static", static, 1, 4),
        ):
            with self.subTest(name):
                service = TreeService(self, files, page_size=10)
                service.delay = 0.1
                limiter = files_sdk.TransferLimiter()
                target = self.scratch / name
                client = self.client(service, transfer_limiter=limiter)
                result = client.file.download_directory(
                    "many",
                    target,
                    max_files=4,
                    max_concurrency=max_concurrency,
                    tuning=tuning,
                )
                self.assertTrue(result.ok)
                self.assertEqual(most, service.max_active)
                for path, data in files.items():
                    self.assertEqual(
                        data, (target / path[len("many/") :]).read_bytes()
                    )
                self.assertEqual(
                    (0, 0), (limiter.parts_in_use, limiter.bytes_in_use)
                )

    def test_a_file_whose_range_buffer_cannot_be_allocated_fails_alone_and_gives_its_place_back(
        self,
    ):
        # One file at a time, adaptive downloads sharing the job's target of
        # one range at once. The first file's range buffer cannot be
        # allocated, once: that file fails with that MemoryError, as its own
        # error, nothing of it is requested, and the place and room it was
        # admitted with go back, so the later files still get the one place.
        files = {
            "many/f{}.bin".format(i): content(800, seed=i) for i in range(3)
        }
        service = TreeService(self, files, page_size=10)
        limiter = files_sdk.TransferLimiter()
        tuning = files_sdk.UploadTuning(
            initial_concurrency=1, grow_every=1000, throughput_window=0
        )
        failure = MemoryError("the range's buffer")
        failures = [failure]
        allocate = bytearray

        def failing_once(*args):
            if failures:
                raise failures.pop()
            return allocate(*args)

        target = self.scratch / "mirror"
        client = self.client(service, transfer_limiter=limiter)
        with mock.patch(
            "files_sdk.download.bytearray", failing_once, create=True
        ):
            # Bounded: a place never given back would end the job here.
            result = client.file.download_directory(
                "many",
                target,
                {"request_timeout": 30},
                max_files=1,
                max_concurrency=1,
                tuning=tuning,
            )
        [failed] = result.failed
        self.assertEqual("many/f0.bin", failed.remote_path)
        self.assertIs(failure, failed.error)
        self.assertNotIn("many/f0.bin", service.downloads)
        self.assertEqual(
            ["many/f1.bin", "many/f2.bin"],
            sorted(o.remote_path for o in result.completed),
        )
        for name in ("many/f1.bin", "many/f2.bin"):
            self.assertEqual(
                files[name], (target / name[len("many/") :]).read_bytes()
            )
        self.assertFalse((target / "f0.bin").exists())
        self.assertEqual((0, 0), (limiter.parts_in_use, limiter.bytes_in_use))

    def test_download_files_downloads_each_pair(self):
        service = TreeService(self, self.FILES)
        pairs = [
            ("docs/a.txt", self.scratch / "one" / "a.txt"),
            ("other/x.txt", str(self.scratch / "x.txt")),
        ]
        result = self.client(service).file.download_files(pairs)
        self.assertTrue(result.ok)
        self.assertEqual(
            (self.scratch / "one" / "a.txt").read_bytes(), b"alpha"
        )
        self.assertEqual((self.scratch / "x.txt").read_bytes(), b"not listed")

    def test_download_files_resumes_skipping_only_files_completed_before(self):
        service = TreeService(self, self.FILES)
        service.fail_paths = {"docs/d.txt"}
        pairs = [
            (name, self.scratch / "out" / name)
            for name in ("docs/a.txt", "docs/d.txt")
        ]
        result = self.client(
            service, max_network_retries=0
        ).file.download_files(pairs, checkpoint=self.checkpoint)
        self.assertEqual(
            [o.remote_path for o in result.failed], ["docs/d.txt"]
        )
        service.fail_paths = set()
        result = self.client(service).file.download_files(
            pairs, checkpoint=self.checkpoint
        )
        self.assertTrue(result.ok)
        reasons = {o.remote_path: o.reason for o in result.completed}
        self.assertEqual(
            reasons, {"docs/a.txt": "completed before", "docs/d.txt": None}
        )
        self.assertEqual(
            (self.scratch / "out" / "docs/d.txt").read_bytes(), b"delta"
        )
        self.assertFalse(self.checkpoint.exists())


class TestJobCheckpointScope(JobTestCase):
    """A job's checkpoint skips a file only when it is for that very pair of
    paths, in the same site and workspace, and nothing about it changed."""

    FILES = {"docs/a.txt": b"alpha", "docs/d.txt": b"delta"}

    def failed_download(self, service, pairs):
        service.fail_paths = {"docs/d.txt"}
        result = self.client(
            service, max_network_retries=0
        ).file.download_files(pairs, checkpoint=self.checkpoint)
        self.assertEqual(
            [o.remote_path for o in result.failed], ["docs/d.txt"]
        )
        service.fail_paths = set()

    @unittest.skipIf(
        sys.platform == "win32",
        "Windows gives no owners or permissions to check",
    )
    def test_a_job_checkpoint_other_users_could_write_is_refused_before_anything_is_skipped_or_fetched(
        self,
    ):
        service = TreeService(self, self.FILES)
        pairs = [
            (name, self.scratch / "out" / name)
            for name in ("docs/a.txt", "docs/d.txt")
        ]
        self.failed_download(service, pairs)
        fetched = list(service.downloads)
        os.chmod(self.checkpoint, 0o666)
        with self.assertRaisesRegex(
            InvalidRequestError, "can be changed by other users"
        ):
            self.client(service).file.download_files(
                pairs, checkpoint=self.checkpoint
            )
        # Nor is a folder download's local folder made.
        never_made = self.scratch / "never-made"
        with self.assertRaisesRegex(
            InvalidRequestError, "can be changed by other users"
        ):
            self.client(service).file.download_directory(
                "docs", never_made, checkpoint=self.checkpoint
            )
        self.assertEqual(service.downloads, fetched)
        self.assertFalse((self.scratch / "out" / "docs/d.txt").exists())
        self.assertFalse(never_made.exists())

    def test_a_changed_destination_is_downloaded_not_skipped(self):
        service = TreeService(self, self.FILES)
        old_a, new_a, d = (
            self.scratch / "old-a",
            self.scratch / "new-a",
            self.scratch / "d",
        )
        self.failed_download(
            service, [("docs/a.txt", old_a), ("docs/d.txt", d)]
        )
        result = self.client(service).file.download_files(
            [("docs/a.txt", new_a), ("docs/d.txt", d)],
            checkpoint=self.checkpoint,
        )
        self.assertTrue(result.ok)
        self.assertEqual(new_a.read_bytes(), b"alpha")
        self.assertEqual([o.reason for o in result.completed], [None, None])

    def test_a_changed_source_is_uploaded_not_skipped(self):
        one, two, bad = (
            self.scratch / "one",
            self.scratch / "two",
            self.scratch / "bad",
        )
        one.write_bytes(b"one")
        two.write_bytes(b"two")
        bad.write_bytes(b"bad")
        # The same size and modification time: only the pair tells them apart.
        os.utime(two, ns=(one.stat().st_atime_ns, one.stat().st_mtime_ns))
        service = UploadService(self, part_size=1000)
        service.refuse_paths = {"y"}
        self.client(service).file.upload_files(
            [(one, "x"), (bad, "y")], checkpoint=self.checkpoint
        )
        service.refuse_paths = set()
        result = self.client(service).file.upload_files(
            [(two, "x"), (bad, "y")], checkpoint=self.checkpoint
        )
        self.assertTrue(result.ok)
        self.assertEqual(service.completed("x"), b"two")
        self.assertEqual([o.reason for o in result.completed], [None, None])

    def test_a_deleted_or_replaced_download_is_downloaded_again(self):
        files = {
            "docs/a.txt": b"alpha",
            "docs/b.txt": b"bravo",
            "docs/d.txt": b"delta",
        }
        service = TreeService(self, files)
        target = self.scratch / "mirror"
        service.fail_paths = {"docs/d.txt"}
        self.client(service, max_network_retries=0).file.download_directory(
            "docs", target, checkpoint=self.checkpoint
        )
        service.fail_paths = set()
        (target / "a.txt").unlink()
        (target / "b.txt").unlink()
        (target / "b.txt").write_bytes(
            b"BRAVO"
        )  # Another file, of the same size.
        result = self.client(service).file.download_directory(
            "docs", target, checkpoint=self.checkpoint
        )
        self.assertTrue(result.ok)
        self.assertEqual(
            {(target / n).read_bytes() for n in ("a.txt", "b.txt", "d.txt")},
            {b"alpha", b"bravo", b"delta"},
        )
        self.assertEqual(
            [o.reason for o in result.completed], [None, None, None]
        )

    def test_a_download_is_skipped_only_while_files_com_offers_the_same_version(
        self,
    ):
        for change in ("same", "changed", "no identity"):
            with self.subTest(change):
                service = TreeService(self, dict(self.FILES))
                target = self.scratch / change
                if change == "no identity":
                    service.legacy = True
                pairs = [
                    ("docs/a.txt", target / "a.txt"),
                    ("docs/d.txt", target / "d.txt"),
                ]
                self.failed_download(service, pairs)
                if change == "changed":
                    service.files["docs/a.txt"] = b"ALPHA"
                result = self.client(service).file.download_files(
                    pairs, checkpoint=self.checkpoint
                )
                self.assertTrue(result.ok)
                reasons = [o.reason for o in result.completed]
                self.assertEqual(
                    reasons,
                    ["completed before" if change == "same" else None, None],
                )
                self.assertEqual(
                    (target / "a.txt").read_bytes(),
                    service.files["docs/a.txt"],
                )
                if change == "same":
                    # Asked whether that version is still offered, by its token only.
                    [check] = [
                        q
                        for path, q in service.negotiations
                        if path == "docs/a.txt"
                        and q.get("expected_download_identity")
                    ]
                    self.assertEqual(
                        check["expected_download_identity"], token_of(b"alpha")
                    )

    def test_a_replaced_or_removed_remote_file_is_uploaded_again(self):
        root = self.tree({"a.txt": b"one", "b.txt": b"two", "c.txt": b"three"})
        service = UploadService(self, part_size=1000)
        service.refuse_paths = {"c.txt"}
        self.client(service).file.upload_directory(
            root, "", checkpoint=self.checkpoint
        )
        service.refuse_paths = set()
        service.replace("a.txt", 3)
        service.remove("b.txt")
        result = self.client(service).file.upload_directory(
            root, "", checkpoint=self.checkpoint
        )
        self.assertTrue(result.ok)
        self.assertEqual(
            [o.reason for o in result.completed], [None, None, None]
        )
        self.assertEqual(service.completed_paths().count("a.txt"), 2)
        self.assertEqual(service.completed_paths().count("b.txt"), 2)

    def test_an_unchanged_upload_is_skipped_after_checking_the_remote_file(
        self,
    ):
        root = self.tree({"a.txt": b"one", "c.txt": b"three"})
        service = UploadService(self, part_size=1000)
        service.refuse_paths = {"c.txt"}
        self.client(service).file.upload_directory(
            root, "", checkpoint=self.checkpoint
        )
        service.refuse_paths = set()
        result = self.client(service).file.upload_directory(
            root, "", checkpoint=self.checkpoint
        )
        self.assertTrue(result.ok)
        self.assertEqual(
            {o.remote_path: o.reason for o in result.completed},
            {"a.txt": "completed before", "c.txt": None},
        )
        self.assertIn("a.txt", service.lookups)
        self.assertEqual(service.completed_paths().count("a.txt"), 1)

    def test_a_checkpoint_of_another_workspace_is_refused(self):
        root = self.tree({"a.txt": b"one", "c.txt": b"three"})
        service = UploadService(self, part_size=1000)
        service.refuse_paths = {"c.txt"}

        def client(**settings):
            made = files_sdk.Client(
                api_key="SECRET-API-KEY",
                base_url=service.url,
                initial_network_retry_delay=0,
                **settings,
            )
            self.addCleanup(made.close)
            return made

        client(workspace_id=1).file.upload_directory(
            root, "", checkpoint=self.checkpoint
        )
        with self.assertRaisesRegex(
            InvalidParameterError, "workspace differs"
        ):
            client(workspace_id=2).file.upload_directory(
                root, "", checkpoint=self.checkpoint
            )
        with self.assertRaisesRegex(
            InvalidParameterError, "workspace differs"
        ):
            client().file.upload_directory(
                root, "", checkpoint=self.checkpoint
            )
        # No credential, or anything made from one, is recorded.
        self.assertNotIn("SECRET", self.checkpoint.read_text())


if __name__ == "__main__":
    unittest.main()

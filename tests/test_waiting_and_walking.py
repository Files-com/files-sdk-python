import time
import unittest

import files_sdk
from files_sdk.error import (
    DeadlineExceededError,
    FileMigrationError,
    InvalidParameterError,
    OperationCancelledError,
)
from tests.download_fixtures import TreeService
from tests.loopback_api import start_loopback_api


class LoopbackTestCase(unittest.TestCase):
    def setUp(self):
        self.api = start_loopback_api(self)
        self.client = files_sdk.Client(
            api_key="key", base_url=self.api.url, max_network_retries=0
        )
        self.addCleanup(self.client.close)

    def paths(self):
        return [
            (request.method, request.path) for request in self.api.requests
        ]


class TestWaitingForFileActions(LoopbackTestCase):
    def migration(self, status, **extra):
        return {
            "id": 7,
            "status": status,
            "operation": "copy",
            "path": "a",
            "dest_path": "b",
            **extra,
        }

    def test_a_pending_copy_is_waited_for_until_its_migration_completes(self):
        self.api.reply_json({"status": "pending", "file_migration_id": 7})
        self.api.reply_json(self.migration("processing", files_moved=1))
        self.api.reply_json(self.migration("completed", files_moved=2))
        seen = []
        started = time.monotonic()
        migration = self.client.file.copy_and_wait(
            "a", {"destination": "b"}, interval=0.05, progress=seen.append
        )
        self.assertIsInstance(
            migration, files_sdk.file_migration.FileMigration
        )
        self.assertEqual(
            (migration.status, migration.files_moved), ("completed", 2)
        )
        self.assertEqual([m.status for m in seen], ["processing", "completed"])
        self.assertEqual(
            self.paths(),
            [
                ("POST", "/file_actions/copy/a"),
                ("GET", "/file_migrations/7"),
                ("GET", "/file_migrations/7"),
            ],
        )
        self.assertGreaterEqual(time.monotonic() - started, 0.05)

    def test_an_action_that_finished_at_once_returns_none_without_polling(
        self,
    ):
        self.api.reply_json({"status": "completed"})
        self.assertIsNone(
            self.client.file.move_and_wait("a", {"destination": "b"})
        )
        self.assertEqual(self.paths(), [("POST", "/file_actions/move/a")])

    def test_a_failed_or_cancelled_migration_raises_with_it(self):
        for status in ("failed", "cancelled"):
            with self.subTest(status=status):
                self.api.requests.clear()
                self.api.reply_json(
                    {"status": "pending", "file_migration_id": 7}
                )
                self.api.reply_json(
                    self.migration(status, failure_message="disk full")
                )
                with self.assertRaises(FileMigrationError) as caught:
                    self.client.file.copy_and_wait(
                        "a", {"destination": "b"}, interval=0.01
                    )
                self.assertEqual(caught.exception.migration.status, status)
                self.assertIn("disk full", str(caught.exception))

    def test_a_file_action_can_be_waited_for_later_with_its_own_client(self):
        self.api.reply_json({"status": "pending", "file_migration_id": 7})
        self.api.reply_json(self.migration("completed"))
        action = self.client.file.copy("a", {"destination": "b"})
        self.assertEqual(action.wait(interval=0.01).status, "completed")
        # The poll uses the client that made the action.
        self.assertEqual(
            self.api.requests[-1].headers.get("X-FilesAPI-Key"), "key"
        )

    def test_the_deadline_bounds_the_wait(self):
        self.api.reply_json({"status": "pending", "file_migration_id": 7})
        for _ in range(50):
            self.api.reply_json(self.migration("processing"))
        started = time.monotonic()
        with self.assertRaises(DeadlineExceededError):
            self.client.file.copy_and_wait(
                "a",
                {"destination": "b"},
                {"request_timeout": 0.3},
                interval=0.05,
            )
        self.assertLess(time.monotonic() - started, 2)

    def test_cancelling_stops_the_wait(self):
        token = files_sdk.CancellationToken()
        self.api.reply_json({"status": "pending", "file_migration_id": 7})
        self.api.reply_json(
            self.migration("processing"), when_received=token.cancel
        )
        with self.assertRaises(OperationCancelledError):
            self.client.file.copy_and_wait(
                "a", {"destination": "b"}, {"cancel_token": token}, interval=5
            )

    def test_an_invalid_interval_is_refused(self):
        self.api.reply_json({"status": "pending", "file_migration_id": 7})
        action = self.client.file.copy("a", {"destination": "b"})
        for interval in (0, -1, float("nan"), "1", True):
            with self.subTest(interval=interval):
                with self.assertRaises(InvalidParameterError):
                    action.wait(interval=interval)  # type: ignore[arg-type]

    def test_delete_and_wait_returns_once_the_path_is_gone(self):
        self.api.reply(204)
        self.api.reply_json({"path": "old", "type": "directory"})
        self.api.reply_json(
            {"type": "not-found", "error": "Not Found", "http-code": 404},
            status=404,
        )
        self.assertIsNone(
            self.client.file.delete_and_wait(
                "old", {"recursive": True}, interval=0.01
            )
        )
        self.assertEqual(
            self.paths(),
            [
                ("DELETE", "/files/old"),
                ("GET", "/file_actions/metadata/old"),
                ("GET", "/file_actions/metadata/old"),
            ],
        )
        # Query booleans keep the form version 1 sent.
        self.assertEqual(self.api.requests[0].query.get("recursive"), "True")


class TestAliases(LoopbackTestCase):
    def test_aliases_return_what_the_operation_they_stand_for_returns(self):
        self.api.reply_json([{"id": 1, "username": "a"}])
        users = self.client.user.all()
        self.assertIsInstance(users, files_sdk.list_obj.ListObj)
        self.assertEqual([user.username for user in users], ["a"])
        self.api.reply(204)
        self.assertIsNone(self.client.user.destroy(1))


class TestWalkingFolders(unittest.TestCase):
    def test_a_folder_tree_is_walked_top_down_a_folder_at_a_time(self):
        service = TreeService(
            self,
            {
                "top/a.txt": b"a",
                "top/one/b.txt": b"b",
                "top/one/deep/c.txt": b"c",
                "top/two/d.txt": b"d",
            },
            folders=["top/empty"],
        )
        client = files_sdk.Client(api_key="key", base_url=service.url)
        self.addCleanup(client.close)
        walked = []
        for folder, folders, files in client.folder.walk("/top/"):
            walked.append(
                (folder, [f.path for f in folders], [f.path for f in files])
            )
            if folder == "top/one":
                folders.clear()  # Skip what is under it.
        self.assertEqual(
            walked,
            [
                ("top", ["top/empty", "top/one", "top/two"], ["top/a.txt"]),
                ("top/empty", [], []),
                ("top/one", ["top/one/deep"], ["top/one/b.txt"]),
                ("top/two", [], ["top/two/d.txt"]),
            ],
        )
        self.assertNotIn(
            "top/one/deep", [folder for folder, _cursor in service.listed]
        )

    def test_the_walk_lists_lazily_and_shares_one_deadline(self):
        service = TreeService(
            self, {"t/{}/f.txt".format(i): b"x" for i in range(5)}
        )
        client = files_sdk.Client(api_key="key", base_url=service.url)
        self.addCleanup(client.close)
        walk = client.folder.walk("t", {"request_timeout": 0.5})
        self.assertEqual(service.listed, [])
        next(walk)
        # Every page of the first folder, and nothing below it yet.
        self.assertEqual(service.listed, [("t", None), ("t", "2"), ("t", "4")])
        time.sleep(0.6)
        with self.assertRaises(DeadlineExceededError):
            next(walk)


if __name__ == "__main__":
    unittest.main()

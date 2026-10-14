import tempfile
import unittest
from pathlib import Path
from urllib.parse import quote

import files_sdk
from tests.loopback_api import serve_loopback_api

DESTINATIONS = (
    ("remote_server", "RemoteServers"),
    ("snapshot", "Snapshots"),
    ("child_site", "Sites"),
)


class TestFileUnderscoreDestinations(unittest.TestCase):
    def setUp(self):
        self.api = serve_loopback_api(self)
        self.client = files_sdk.Client(
            api_key="clientkey", base_url=self.api.url
        )
        self.addCleanup(self.client.close)

    def callers(self):
        """The module functions, and the same helpers of a client."""
        return (
            ("module", files_sdk, "globalkey"),
            ("client", self.client.file, "clientkey"),
        )

    def test_copy_and_move_send_the_normalized_destination(self):
        for label, owner, key in self.callers():
            for name, root in DESTINATIONS:
                for action in ("copy", "move"):
                    with self.subTest(
                        caller=label, helper=f"{action}_to_{name}"
                    ):
                        self.api.reply_json({"status": "completed"})
                        params = {"overwrite": True}
                        getattr(owner, f"{action}_to_{name}")(
                            "source.txt",
                            42,
                            "/../../remote\\path//./to/file.txt",
                            params,
                        )

                        request = self.api.requests.pop()
                        self.assertEqual(
                            ("POST", f"/file_actions/{action}/source.txt"),
                            (request.method, request.path),
                        )
                        self.assertEqual(
                            f"_/{root}/42/remote/path/to/file.txt",
                            request.json["destination"],
                        )
                        self.assertTrue(request.json["overwrite"])
                        self.assertEqual(
                            key, request.headers["X-FilesAPI-Key"]
                        )
                        self.assertEqual({"overwrite": True}, params)

    def test_uploads_go_to_the_normalized_destination_in_one_operation(self):
        with tempfile.TemporaryDirectory() as directory:
            local = Path(directory) / "file.txt"
            local.write_bytes(b"hello")
            for label, owner, key in self.callers():
                for name, root in DESTINATIONS:
                    with self.subTest(
                        caller=label, helper=f"upload_to_{name}"
                    ):
                        destination = f"_/{root}/42/file.txt"
                        self.api.reply_json(
                            [
                                {
                                    "ref": "ref1",
                                    "part_number": 1,
                                    "partsize": 1024,
                                    "http_method": "PUT",
                                    "upload_uri": self.api.url
                                    + "/storage/part1?X-Amz-Signature=secret",
                                }
                            ]
                        )
                        self.api.reply(200, headers={"ETag": '"etag1"'})
                        self.api.reply_json({"path": destination, "size": 5})

                        getattr(owner, f"upload_to_{name}")(str(local), 42)

                        begin, part, finish = self.api.wait_for_requests(3)
                        self.api.requests.clear()
                        self.assertEqual(
                            f"/file_actions/begin_upload/{quote(destination, safe='')}",
                            begin.path,
                        )
                        self.assertEqual(
                            ("PUT", "/storage/part1", b"hello"),
                            (part.method, part.url_path, part.body),
                        )
                        self.assertNotIn("X-FilesAPI-Key", part.headers)
                        self.assertEqual(
                            f"/files/{quote(destination, safe='')}",
                            finish.path,
                        )
                        self.assertEqual(
                            {
                                "action": "end",
                                "etags": [{"etag": "etag1", "part": 1}],
                                "ref": "ref1",
                                "size": 5,
                            },
                            {
                                k: finish.json[k]
                                for k in ("action", "etags", "ref", "size")
                            },
                        )
                        self.assertEqual(
                            [key, key],
                            [
                                begin.headers["X-FilesAPI-Key"],
                                finish.headers["X-FilesAPI-Key"],
                            ],
                        )


if __name__ == "__main__":
    unittest.main()

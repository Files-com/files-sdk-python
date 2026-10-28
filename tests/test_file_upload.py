"""Closing a file written with files_sdk.file.open, against the shared mock
server's simulator.

The scenarios task (python scripts/tasks.py scenarios) runs these tests in
its file-upload run: the launcher starts a server for that run alone under
the api-scenarios-canonical preset and sets FILES_MOCK_SERVER_URL,
FILES_MOCK_API_KEY, FILES_MOCK_INSTANCE, FILES_MOCK_SCHEMA_SHA256 and
FILES_MOCK_SCENARIO_FILE. Run without that URL, these tests are skipped;
the scenarios task fails when they are.

Before any control, each test checks that the server is the launcher's
own; it then resets it to the preset's own reset, so the journal and the
fault rules hold only that test's requests. The journal numbers API keys
in the order they first arrive and never holds their values.
"""

import hashlib
import json
import os
import unittest
import urllib.request
from unittest.mock import patch

import files_sdk
from files_sdk.error import APIError

SERVER_URL = os.environ.get("FILES_MOCK_SERVER_URL")
CONTROL = "/__files_mock/v1"
PAYLOAD = b"\x00\xff\r\n" * 2048
PAYLOAD_SHA256 = hashlib.sha256(PAYLOAD).hexdigest()
REMOTE_PATH = "remote.bin"
# The key the upload's own options give, not the module's.
OPTIONS_KEY = "optionsKey"
# Requests go to the launcher's address itself, never through a proxy.
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def call(method, path, body=None, api_key=None):
    """The status and JSON answer of one request to the server."""
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(
        SERVER_URL + path, data=data, method=method
    )
    if data is not None:
        request.add_header("Content-Type", "application/json")
    if api_key is not None:
        request.add_header("X-FilesAPI-Key", api_key)
    with OPENER.open(request, timeout=30) as response:
        answer = response.read()
        return response.status, json.loads(answer) if answer else None


@unittest.skipUnless(
    SERVER_URL,
    "needs the shared mock server's api-scenarios-canonical preset: "
    "python scripts/tasks.py scenarios",
)
class TestFileUpload(unittest.TestCase):
    def setUp(self):
        self.ready()
        with open(
            os.environ["FILES_MOCK_SCENARIO_FILE"], encoding="utf-8"
        ) as scenario:
            reset = json.load(scenario)["reset"]
        _, answer = call("POST", CONTROL + "/reset", reset)
        self.epoch = answer["epoch"]
        self.assertEqual(self.epoch, self.ready()["epoch"])
        self.key = os.environ["FILES_MOCK_API_KEY"]
        # The server, the run's key as the module's own, and a retry for a
        # failed request, as before: a completion is still sent only once.
        for name, value in {
            "base_url": SERVER_URL,
            "the_api_key": self.key,
            "session_id": None,
            "workspace_id": None,
            "max_network_retries": 1,
        }.items():
            patcher = patch.object(files_sdk, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(files_sdk.close)

    def ready(self):
        """The server's readiness, once it shows the launcher's own server:
        this run's instance, in simulation mode, contract 3 and the schema
        the launcher checked. Another server, such as another service on
        its port, fails the test before any control reaches it."""
        _, ready = call("GET", CONTROL + "/ready")
        self.assertEqual(
            (
                "ready",
                "simulation",
                3,
                os.environ["FILES_MOCK_SCHEMA_SHA256"],
                os.environ["FILES_MOCK_INSTANCE"],
            ),
            (
                ready["status"],
                ready["mode"],
                ready["contract_version"],
                ready["schema_sha256"],
                ready["instance"],
            ),
        )
        return ready

    def journal(self, *operations):
        """The API requests of this test's epoch, oldest first, once the
        journal shows it holds every one and they were of operations, in
        that order."""
        _, journal = call("GET", CONTROL + "/journal")
        self.assertEqual(
            (self.epoch, True, 0),
            (journal["epoch"], journal["complete"], journal["dropped"]),
        )
        entries = journal["entries"]
        self.assertEqual(
            list(operations), [entry["operation"] for entry in entries]
        )
        return entries

    def namespace(self):
        """How many files and folders the server holds now, still in this
        test's epoch."""
        ready = self.ready()
        self.assertEqual(self.epoch, ready["epoch"])
        state = ready["namespace"]["state"]
        return state["files"], state["folders"]

    def number_keys(self):
        """Has the module's key numbered 1 and the options' key 2, each by a
        listing of the root that carries it, before the SDK sends either:
        the journal then names either key by that number when the SDK sends
        it, and any other key by a number of its own."""
        for key in (self.key, OPTIONS_KEY):
            status, _ = call("GET", "/api/rest/v1/folders/", api_key=key)
            self.assertEqual(200, status)

    def delete_own_file(self, path):
        """Deletes the file the test published, which leaves the namespace
        as the reset left it: empty."""
        status, _ = call(
            "DELETE", "/api/rest/v1/files/" + path, api_key=self.key
        )
        self.assertEqual(204, status)
        self.assertEqual((0, 0), self.namespace())

    def open_with_payload(self):
        f = files_sdk.file.open(REMOTE_PATH, "wb", {"api_key": OPTIONS_KEY})
        f.write(PAYLOAD)
        return f

    def test_close_finalizes_once_and_releases_the_write_buffer(self):
        self.number_keys()
        f = self.open_with_payload()
        write_buffer = f.io_obj

        f.close()
        f.close()

        self.addCleanup(self.delete_own_file, REMOTE_PATH)
        entries = self.journal(
            "folders.list",
            "folders.list",
            "files.begin_upload",
            "transfers.upload_part",
            "files.finalize_upload",
        )
        module_listing, options_listing, begin, part, finalization = entries
        # The listings numbered the module's key 1 and the options' key 2.
        # The upload is begun and completed with exactly the options' key,
        # not the module's, since any other key would have a number of its
        # own; the part goes to storage with no key.
        self.assertEqual({"api_key": 1}, module_listing["credentials"])
        self.assertEqual({"api_key": 2}, options_listing["credentials"])
        self.assertEqual({"api_key": 2}, begin["credentials"])
        self.assertEqual({"api_key": 2}, finalization["credentials"])
        self.assertNotIn("credentials", part)
        self.assertEqual(200, begin["status"])
        self.assertEqual(
            (200, begin["upload"], 1, len(PAYLOAD), PAYLOAD_SHA256),
            (
                part["status"],
                part["upload"],
                part["part"],
                part["bytes"],
                part["sha256"],
            ),
        )
        # The simulator completes an upload only for action=end, its own
        # ref, etags that list its parts and a size they hold: the one
        # completion, of this upload, published exactly what was written.
        self.assertEqual(
            (201, begin["upload"], len(PAYLOAD), PAYLOAD_SHA256),
            (
                finalization["status"],
                finalization["upload"],
                finalization["bytes"],
                finalization["sha256"],
            ),
        )
        wire = finalization["wire"]
        self.assertEqual(
            ("string", "string", "array", "number"),
            (wire["action"], wire["ref"], wire["etags"], wire["size"]),
        )
        # An upload like this one may also be completed without etags; the
        # SDK's list its one part.
        self.assertEqual(
            {"count": 1, "types": ["object"]},
            finalization["wire_elements"]["etags"],
        )
        self.assertEqual(f.size, len(PAYLOAD))
        self.assertTrue(f.closed)
        self.assertTrue(write_buffer.closed)
        self.assertTrue(f.io_obj.closed)

    def test_failed_finalization_ends_the_upload_without_completing_it_again(
        self,
    ):
        # Version 2 holds at most one part of what was written, and never
        # sends again a completion that may have taken effect, so a failed
        # close() raises its error, releases the buffer and ends the upload.
        # Version 1 kept the whole buffer open, and closing again could
        # complete the upload twice. See UPGRADING.md.
        call(
            "POST",
            CONTROL + "/faults",
            {
                "operation": "files.finalize_upload",
                "match": {"path": REMOTE_PATH},
                "status": 503,
            },
        )
        self.assertEqual(1, self.ready()["state"]["pending_faults"])
        f = self.open_with_payload()
        write_buffer = f.io_obj

        with self.assertRaises(APIError) as caught:
            f.close()

        self.assertEqual(caught.exception.http_status, 503)
        self.assertTrue(caught.exception.remote_outcome_unknown)
        self.assertTrue(f.closed)
        self.assertTrue(write_buffer.closed)
        f.close()
        with self.assertRaises(ValueError):
            f.write(b"more")
        begin, part, attempt = self.journal(
            "files.begin_upload",
            "transfers.upload_part",
            "files.finalize_upload",
        )
        self.assertEqual(200, begin["status"])
        self.assertNotIn("credentials", part)
        self.assertEqual(
            (200, begin["upload"], len(PAYLOAD), PAYLOAD_SHA256),
            (part["status"], part["upload"], part["bytes"], part["sha256"]),
        )
        # The one completion sent met the rule, which refused it before
        # anything was applied; it carried an action, a ref and a size, as
        # the completed one does.
        wire = attempt["wire"]
        self.assertEqual(
            (503, "string", "string", "number"),
            (attempt["status"], wire["action"], wire["ref"], wire["size"]),
        )
        self.assertIsNotNone(attempt["fault_id"])
        # The rule was used, and nothing was published.
        self.assertEqual(0, self.ready()["state"]["pending_faults"])
        self.assertEqual((0, 0), self.namespace())


if __name__ == "__main__":
    unittest.main()

"""Folder listing against the shared mock server's folder-list scenario.

The scenario's launcher (python scripts/tasks.py scenarios) starts the
server and sets FILES_MOCK_SERVER_URL, FILES_MOCK_API_KEY and
FILES_MOCK_SCENARIO_FILE, which names the parent folder, its child folders
in listing order and the page size. Run without that URL, these tests are
skipped; with it, anything missing or wrong fails them.

test_list_pagination.py keeps the pages the shared server must not
produce, such as empty, malformed or repeated ones.
"""

import json
import logging
import math
import os
import unittest
from unittest.mock import patch

import files_sdk

SERVER_URL = os.environ.get("FILES_MOCK_SERVER_URL")


def auto_paging(pager):
    return list(pager.auto_paging_iter())


def documented_manual_loop(pager):
    items = []
    while True:
        items.extend(pager)
        if not pager.has_next_page:
            break
        pager.load_next_page()
    return items


@unittest.skipUnless(
    SERVER_URL,
    "needs the shared mock server's folder-list scenario: "
    "python scripts/tasks.py scenarios",
)
class TestSharedFolderList(unittest.TestCase):
    def setUp(self):
        with open(
            os.environ["FILES_MOCK_SCENARIO_FILE"], encoding="utf-8"
        ) as scenario:
            expected = json.load(scenario)
        self.parent = expected["parent"]
        self.children = expected["children"]
        self.per_page = expected["per_page"]
        self.options = {"api_key": os.environ["FILES_MOCK_API_KEY"]}
        # Only the scenario's server and key, and one attempt a request, so
        # the server sees exactly the pages the client asked for.
        for name, value in {
            "base_url": SERVER_URL,
            "the_api_key": None,
            "session_id": None,
            "workspace_id": None,
            "max_network_retries": 0,
        }.items():
            patcher = patch.object(files_sdk, name, value)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(files_sdk.close)

    def list_parent(self, walk, params):
        """The items walk reads from a new list of the parent, and the
        number of requests the SDK logged sending for it."""
        with self.assertLogs("files_sdk", logging.INFO) as logs:
            items = walk(
                files_sdk.folder.list_for(self.parent, params, self.options)
            )
        requests = [
            record
            for record in logs.records
            if record.getMessage().startswith("message=Request ")
        ]
        return items, len(requests)

    def test_every_page_lists_the_child_folders_in_order(self):
        pages = math.ceil(len(self.children) / self.per_page)
        for params in (
            {"per_page": self.per_page},
            {"per_page": self.per_page, "with_previews": True},
        ):
            for walk in (auto_paging, documented_manual_loop):
                with self.subTest(walk=walk.__name__, params=params):
                    items, requests = self.list_parent(walk, params)

                    self.assertEqual(
                        self.children, [item.path for item in items]
                    )
                    self.assertEqual(
                        ["directory"] * len(self.children),
                        [item.type for item in items],
                    )
                    self.assertEqual(pages, requests)


if __name__ == "__main__":
    unittest.main()

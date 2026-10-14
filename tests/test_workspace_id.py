import unittest

import files_sdk
from tests.loopback_api import serve_loopback_api


class TestWorkspaceId(unittest.TestCase):
    def setUp(self):
        self.api = serve_loopback_api(self)
        files_sdk.set_workspace_id(None)
        self.addCleanup(files_sdk.set_workspace_id, None)

    def workspace_header(self, options=None):
        self.api.reply_json([])
        files_sdk.folder.list_for("/", {}, options)
        return self.api.requests.pop().headers.get("X-Files-Workspace-Id")

    def test_the_module_workspace_is_sent_and_an_option_overrides_it(self):
        files_sdk.set_workspace_id(123)

        self.assertEqual("123", self.workspace_header())
        self.assertEqual("456", self.workspace_header({"workspace_id": 456}))

    def test_workspace_zero_is_a_workspace(self):
        self.assertEqual("0", self.workspace_header({"workspace_id": 0}))
        files_sdk.set_workspace_id(0)
        self.assertEqual("0", self.workspace_header())

    def test_no_workspace_sends_no_header(self):
        self.assertIsNone(self.workspace_header())

    def test_clear_and_an_empty_string_remove_the_module_workspace(self):
        files_sdk.set_workspace_id(123)

        self.assertIsNone(
            self.workspace_header({"workspace_id": files_sdk.CLEAR})
        )
        self.assertIsNone(self.workspace_header({"workspace_id": ""}))


if __name__ == "__main__":
    unittest.main()

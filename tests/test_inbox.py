import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Inbox
from files_sdk import inbox

class InboxTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/inboxes"), "Mock path does not exist")
    def test_list(self):
        resp = inbox.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/inboxes/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = inbox.create_export()

if __name__ == '__main__':
    unittest.main()
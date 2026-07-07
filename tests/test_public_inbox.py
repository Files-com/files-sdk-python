import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PublicInbox
from files_sdk import public_inbox

class PublicInboxTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/public_inboxes"), "Mock path does not exist")
    def test_list(self):
        resp = public_inbox.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/public_inboxes/key/{key}"), "Mock path does not exist")
    def test_get_key(self):
        key = "foo"
        params = {
            "key" : "foo",
        }
        public_inbox.get_key(key, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/public_inboxes/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = public_inbox.create_export()

if __name__ == '__main__':
    unittest.main()
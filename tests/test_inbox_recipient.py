import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import InboxRecipient
from files_sdk import inbox_recipient

class InboxRecipientTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/inbox_recipients"), "Mock path does not exist")
    def test_list(self):
        params = {
            "inbox_id" : 12345,
        }
        inbox_recipient.list(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/inbox_recipients"), "Mock path does not exist")
    def test_create(self):
        params = {
            "inbox_id" : 12345,
            "recipient" : "foo",
        }
        inbox_recipient.create(params)

if __name__ == '__main__':
    unittest.main()
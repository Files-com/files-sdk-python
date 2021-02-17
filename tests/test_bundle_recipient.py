import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import BundleRecipient
from files_sdk import bundle_recipient

class BundleRecipientTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bundle_recipients"), "Mock path does not exist")
    def test_list(self):
        params = {
            "bundle_id" : 12345,
        }
        bundle_recipient.list(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/bundle_recipients"), "Mock path does not exist")
    def test_create(self):
        params = {
            "bundle_id" : 12345,
            "recipient" : "foo",
        }
        bundle_recipient.create(params)

if __name__ == '__main__':
    unittest.main()
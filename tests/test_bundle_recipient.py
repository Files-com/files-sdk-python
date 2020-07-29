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
    def test_list(self):
        params = {
            "bundle_id" : 12345,
        }
        bundle_recipient.list(params)

if __name__ == '__main__':
    unittest.main()
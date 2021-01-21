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
    def test_list(self):
        params = {
            "inbox_id" : 12345,
        }
        inbox_recipient.list(params)

    def test_create(self):
        params = {
            "inbox_id" : 12345,
            "recipient" : "foo",
        }
        inbox_recipient.create(params)

if __name__ == '__main__':
    unittest.main()
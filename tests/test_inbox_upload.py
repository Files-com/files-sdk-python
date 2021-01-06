import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import InboxUpload
from files_sdk import inbox_upload

class InboxUploadTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        resp = inbox_upload.list()

if __name__ == '__main__':
    unittest.main()
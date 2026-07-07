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
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/inbox_uploads"), "Mock path does not exist")
    def test_list(self):
        resp = inbox_upload.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/inbox_uploads/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = inbox_upload.create_export()

if __name__ == '__main__':
    unittest.main()
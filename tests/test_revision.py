import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Revision
from files_sdk import revision

class RevisionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/revisions"), "Mock path does not exist")
    def test_list(self):
        resp = revision.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/revisions/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = revision.create_export()

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Restore
from files_sdk import restore

class RestoreTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/restores"), "Mock path does not exist")
    def test_list(self):
        resp = restore.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/restores"), "Mock path does not exist")
    def test_create(self):
        params = {
            "earliest_date" : "foo",
        }
        restore.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/restores/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = restore.create_export()

if __name__ == '__main__':
    unittest.main()
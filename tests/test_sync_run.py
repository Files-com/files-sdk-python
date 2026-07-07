import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SyncRun
from files_sdk import sync_run

class SyncRunTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/sync_runs"), "Mock path does not exist")
    def test_list(self):
        resp = sync_run.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/sync_runs/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sync_run.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sync_runs/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = sync_run.create_export()

if __name__ == '__main__':
    unittest.main()
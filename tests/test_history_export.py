import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import HistoryExport
from files_sdk import history_export

class HistoryExportTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/history_exports/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        history_export.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/history_exports"), "Mock path does not exist")
    def test_create(self):
        resp = history_export.create()

if __name__ == '__main__':
    unittest.main()
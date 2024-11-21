import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Export
from files_sdk import export

class ExportTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/exports"), "Mock path does not exist")
    def test_list(self):
        resp = export.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/exports/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        export.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/exports/create_export"), "Mock path does not exist")
    def test_create(self):
        resp = export.create()

if __name__ == '__main__':
    unittest.main()
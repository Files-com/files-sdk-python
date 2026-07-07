import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Preview
from files_sdk import preview

class PreviewTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/previews"), "Mock path does not exist")
    def test_list(self):
        params = {
            "ids" : "foo",
        }
        preview.list(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/previews/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        preview.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/previews/create_export"), "Mock path does not exist")
    def test_create_export(self):
        params = {
            "ids" : "foo",
        }
        preview.create_export(params)

if __name__ == '__main__':
    unittest.main()
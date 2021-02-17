import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Folder
from files_sdk import folder

class FolderTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/folders/{path}"), "Mock path does not exist")
    def test_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        folder.list_for(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/folders/{path}"), "Mock path does not exist")
    def test_create(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        folder.create(path, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Priority
from files_sdk import priority

class PriorityTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/priorities"), "Mock path does not exist")
    def test_list(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        priority.list(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/priorities/create_export"), "Mock path does not exist")
    def test_create_export(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        priority.create_export(path, params)

if __name__ == '__main__':
    unittest.main()
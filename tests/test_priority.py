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

if __name__ == '__main__':
    unittest.main()
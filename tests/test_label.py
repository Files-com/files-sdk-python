import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Label
from files_sdk import label

class LabelTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/labels"), "Mock path does not exist")
    def test_list(self):
        resp = label.list()

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Warning
from files_sdk import warning

class WarningTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/warnings"), "Mock path does not exist")
    def test_list(self):
        resp = warning.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/warnings/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = warning.create_export()

if __name__ == '__main__':
    unittest.main()
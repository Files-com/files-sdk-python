import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import App
from files_sdk import app

class AppTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/apps"), "Mock path does not exist")
    def test_list(self):
        resp = app.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/apps/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = app.create_export()

if __name__ == '__main__':
    unittest.main()
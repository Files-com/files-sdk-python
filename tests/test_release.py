import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Release
from files_sdk import release

class ReleaseTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/releases/latest"), "Mock path does not exist")
    def test_get_latest(self):
        resp = release.get_latest()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/releases"), "Mock path does not exist")
    def test_create(self):
        resp = release.create()

if __name__ == '__main__':
    unittest.main()
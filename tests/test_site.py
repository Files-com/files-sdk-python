import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Site
from files_sdk import site

class SiteTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site"), "Mock path does not exist")
    def test_get(self):
        resp = site.get()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site/usage"), "Mock path does not exist")
    def test_get_usage(self):
        resp = site.get_usage()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/site"), "Mock path does not exist")
    def test_update(self):
        resp = site.update()

if __name__ == '__main__':
    unittest.main()
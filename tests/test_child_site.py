import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ChildSite
from files_sdk import child_site

class ChildSiteTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/child_sites"), "Mock path does not exist")
    def test_list(self):
        resp = child_site.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/child_sites"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        child_site.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/child_sites/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = child_site.create_export()

if __name__ == '__main__':
    unittest.main()
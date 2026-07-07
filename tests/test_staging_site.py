import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import StagingSite
from files_sdk import staging_site

class StagingSiteTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/staging_sites"), "Mock path does not exist")
    def test_list(self):
        resp = staging_site.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/staging_sites"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "email" : "foo",
        }
        staging_site.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/staging_sites/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = staging_site.create_export()

if __name__ == '__main__':
    unittest.main()
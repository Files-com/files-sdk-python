import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PartnerSite
from files_sdk import partner_site

class PartnerSiteTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partner_sites"), "Mock path does not exist")
    def test_list(self):
        resp = partner_site.list()

if __name__ == '__main__':
    unittest.main()
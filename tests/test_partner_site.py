import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PartnerSite
from files_sdk import partner_site

class PartnerSiteTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partner_sites/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        partner_site = PartnerSite(params)
        partner_site.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partner_sites/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_site.delete(id, params)

if __name__ == '__main__':
    unittest.main()
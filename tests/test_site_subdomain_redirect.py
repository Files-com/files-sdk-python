import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SiteSubdomainRedirect
from files_sdk import site_subdomain_redirect

class SiteSubdomainRedirectTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/site_subdomain_redirects/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        site_subdomain_redirect = SiteSubdomainRedirect(params)
        site_subdomain_redirect.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site_subdomain_redirects"), "Mock path does not exist")
    def test_list(self):
        resp = site_subdomain_redirect.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site_subdomain_redirects/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        site_subdomain_redirect.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/site_subdomain_redirects/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        site_subdomain_redirect.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
from tests.base import TestBase
from files_sdk.models import SiteSubdomainRedirect
from files_sdk import site_subdomain_redirect


class SiteSubdomainRedirectTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        site_subdomain_redirect = SiteSubdomainRedirect(params)
        site_subdomain_redirect.delete(params)
        self.assert_typed(site_subdomain_redirect)

    # Static Methods
    def test_list(self):
        result = site_subdomain_redirect.list()
        self.assert_returns(site_subdomain_redirect.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = site_subdomain_redirect.find(id, params)
        self.assert_returns(site_subdomain_redirect.find, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = site_subdomain_redirect.delete(id, params)
        self.assert_returns(site_subdomain_redirect.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

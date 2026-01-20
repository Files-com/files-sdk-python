import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PartnerSiteRequest
from files_sdk import partner_site_request

class PartnerSiteRequestTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/partner_site_requests/{id}/reject"), "Mock path does not exist")
    def test_reject(self):
        params = {
            "id" : 12345,
        }
        partner_site_request = PartnerSiteRequest(params)
        partner_site_request.reject(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/partner_site_requests/{id}/approve"), "Mock path does not exist")
    def test_approve(self):
        params = {
            "id" : 12345,
        }
        partner_site_request = PartnerSiteRequest(params)
        partner_site_request.approve(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partner_site_requests/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        partner_site_request = PartnerSiteRequest(params)
        partner_site_request.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partner_site_requests"), "Mock path does not exist")
    def test_list(self):
        resp = partner_site_request.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partner_site_requests/find_by_pairing_key"), "Mock path does not exist")
    def test_find_by_pairing_key(self):
        params = {
            "pairing_key" : "foo",
        }
        partner_site_request.find_by_pairing_key(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/partner_site_requests"), "Mock path does not exist")
    def test_create(self):
        params = {
            "partner_id" : 12345,
            "site_url" : "foo",
        }
        partner_site_request.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/partner_site_requests/{id}/reject"), "Mock path does not exist")
    def test_reject(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_site_request.reject(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/partner_site_requests/{id}/approve"), "Mock path does not exist")
    def test_approve(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_site_request.approve(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partner_site_requests/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_site_request.delete(id, params)

if __name__ == '__main__':
    unittest.main()
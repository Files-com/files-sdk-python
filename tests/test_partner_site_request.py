import unittest
from tests.base import TestBase
from files_sdk.models import PartnerSiteRequest
from files_sdk import partner_site_request


class PartnerSiteRequestTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        partner_site_request = PartnerSiteRequest(params)
        partner_site_request.delete(params)
        self.assert_typed(partner_site_request)

    # Static Methods
    def test_list(self):
        result = partner_site_request.list()
        self.assert_returns(partner_site_request.list, result)
        self.assert_typed(result)

    def test_find_by_pairing_key(self):
        params = {
            "pairing_key": "foo",
        }
        result = partner_site_request.find_by_pairing_key(params)
        self.assert_returns(partner_site_request.find_by_pairing_key, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "host_partner_id": 12345,
            "guest_site_url": "foo",
        }
        result = partner_site_request.create(params)
        self.assert_returns(partner_site_request.create, result)
        self.assert_typed(result)

    def test_reject(self):
        params = {
            "pairing_key": "foo",
        }
        result = partner_site_request.reject(params)
        self.assert_returns(partner_site_request.reject, result)
        self.assert_typed(result)

    def test_approve(self):
        params = {
            "pairing_key": "foo",
        }
        result = partner_site_request.approve(params)
        self.assert_returns(partner_site_request.approve, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner_site_request.delete(id, params)
        self.assert_returns(partner_site_request.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

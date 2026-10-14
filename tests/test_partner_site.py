import unittest
from tests.base import TestBase
from files_sdk.models import PartnerSite
from files_sdk import partner_site


class PartnerSiteTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        partner_site = PartnerSite(params)
        partner_site.id = params["id"]
        partner_site.delete(params)
        self.assert_typed(partner_site)

    # Static Methods
    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner_site.delete(id, params)
        self.assert_returns(partner_site.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

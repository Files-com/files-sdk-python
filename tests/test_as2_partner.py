import unittest
from tests.base import TestBase
from files_sdk.models import As2Partner
from files_sdk import as2_partner


class As2PartnerTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        as2_partner = As2Partner(params)
        result = as2_partner.update(params)
        self.assert_returns(As2Partner.update, result)
        self.assert_typed(as2_partner)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        as2_partner = As2Partner(params)
        as2_partner.delete(params)
        self.assert_typed(as2_partner)

    # Static Methods
    def test_list(self):
        result = as2_partner.list()
        self.assert_returns(as2_partner.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = as2_partner.find(id, params)
        self.assert_returns(as2_partner.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "as2_station_id": 12345,
            "name": "foo",
            "uri": "foo",
        }
        result = as2_partner.create(params)
        self.assert_returns(as2_partner.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = as2_partner.update(id, params)
        self.assert_returns(as2_partner.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = as2_partner.delete(id, params)
        self.assert_returns(as2_partner.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk.models import Partner
from files_sdk import partner


class PartnerTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        partner = Partner(params)
        result = partner.update(params)
        self.assert_returns(Partner.update, result)
        self.assert_typed(partner)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        partner = Partner(params)
        partner.delete(params)
        self.assert_typed(partner)

    # Static Methods
    def test_list(self):
        result = partner.list()
        self.assert_returns(partner.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner.find(id, params)
        self.assert_returns(partner.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "root_folder": "foo",
        }
        result = partner.create(params)
        self.assert_returns(partner.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner.update(id, params)
        self.assert_returns(partner.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner.delete(id, params)
        self.assert_returns(partner.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

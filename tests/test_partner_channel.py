import unittest
from tests.base import TestBase
from files_sdk.models import PartnerChannel
from files_sdk import partner_channel


class PartnerChannelTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        partner_channel = PartnerChannel(params)
        result = partner_channel.update(params)
        self.assert_returns(PartnerChannel.update, result)
        self.assert_typed(partner_channel)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        partner_channel = PartnerChannel(params)
        partner_channel.delete(params)
        self.assert_typed(partner_channel)

    # Static Methods
    def test_list(self):
        result = partner_channel.list()
        self.assert_returns(partner_channel.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner_channel.find(id, params)
        self.assert_returns(partner_channel.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "partner_id": 12345,
            "path": "foo",
        }
        result = partner_channel.create(params)
        self.assert_returns(partner_channel.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner_channel.update(id, params)
        self.assert_returns(partner_channel.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner_channel.delete(id, params)
        self.assert_returns(partner_channel.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

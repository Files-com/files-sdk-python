import unittest
from tests.base import TestBase
from files_sdk.models import PartnerChannelTemplate
from files_sdk import partner_channel_template


class PartnerChannelTemplateTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        partner_channel_template = PartnerChannelTemplate(params)
        result = partner_channel_template.update(params)
        self.assert_returns(PartnerChannelTemplate.update, result)
        self.assert_typed(partner_channel_template)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        partner_channel_template = PartnerChannelTemplate(params)
        partner_channel_template.delete(params)
        self.assert_typed(partner_channel_template)

    # Static Methods
    def test_list(self):
        result = partner_channel_template.list()
        self.assert_returns(partner_channel_template.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner_channel_template.find(id, params)
        self.assert_returns(partner_channel_template.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "path": "foo",
        }
        result = partner_channel_template.create(params)
        self.assert_returns(partner_channel_template.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner_channel_template.update(id, params)
        self.assert_returns(partner_channel_template.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = partner_channel_template.delete(id, params)
        self.assert_returns(partner_channel_template.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

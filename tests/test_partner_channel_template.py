import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PartnerChannelTemplate
from files_sdk import partner_channel_template

class PartnerChannelTemplateTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/partner_channel_templates/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        partner_channel_template = PartnerChannelTemplate(params)
        partner_channel_template.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partner_channel_templates/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        partner_channel_template = PartnerChannelTemplate(params)
        partner_channel_template.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partner_channel_templates"), "Mock path does not exist")
    def test_list(self):
        resp = partner_channel_template.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partner_channel_templates/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_channel_template.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/partner_channel_templates"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "path" : "foo",
        }
        partner_channel_template.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/partner_channel_templates/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_channel_template.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partner_channel_templates/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_channel_template.delete(id, params)

if __name__ == '__main__':
    unittest.main()
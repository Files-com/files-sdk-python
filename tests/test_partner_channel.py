import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PartnerChannel
from files_sdk import partner_channel

class PartnerChannelTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/partner_channels/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        partner_channel = PartnerChannel(params)
        partner_channel.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partner_channels/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        partner_channel = PartnerChannel(params)
        partner_channel.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partner_channels"), "Mock path does not exist")
    def test_list(self):
        resp = partner_channel.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partner_channels/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_channel.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/partner_channels"), "Mock path does not exist")
    def test_create(self):
        params = {
            "partner_id" : 12345,
            "path" : "foo",
        }
        partner_channel.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/partner_channels/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_channel.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partner_channels/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner_channel.delete(id, params)

if __name__ == '__main__':
    unittest.main()
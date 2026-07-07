import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import EventChannel
from files_sdk import event_channel

class EventChannelTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/event_channels/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        event_channel = EventChannel(params)
        event_channel.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/event_channels/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        event_channel = EventChannel(params)
        event_channel.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_channels"), "Mock path does not exist")
    def test_list(self):
        resp = event_channel.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_channels/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_channel.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/event_channels"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        event_channel.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/event_channels/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = event_channel.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/event_channels/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_channel.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/event_channels/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_channel.delete(id, params)

if __name__ == '__main__':
    unittest.main()
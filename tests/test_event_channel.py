import unittest
from tests.base import TestBase
from files_sdk.models import EventChannel
from files_sdk import event_channel


class EventChannelTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        event_channel = EventChannel(params)
        result = event_channel.update(params)
        self.assert_returns(EventChannel.update, result)
        self.assert_typed(event_channel)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        event_channel = EventChannel(params)
        event_channel.delete(params)
        self.assert_typed(event_channel)

    # Static Methods
    def test_list(self):
        result = event_channel.list()
        self.assert_returns(event_channel.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_channel.find(id, params)
        self.assert_returns(event_channel.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
        }
        result = event_channel.create(params)
        self.assert_returns(event_channel.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_channel.update(id, params)
        self.assert_returns(event_channel.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_channel.delete(id, params)
        self.assert_returns(event_channel.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk.models import As2IncomingMessage
from files_sdk import as2_incoming_message


class As2IncomingMessageTest(TestBase):
    # Instance Methods
    def test_instance_replay(self):
        params = {
            "id": 12345,
        }
        as2_incoming_message = As2IncomingMessage(params)
        result = as2_incoming_message.replay(params)
        self.assert_returns(As2IncomingMessage.replay, result)
        self.assert_typed(as2_incoming_message)

    # Static Methods
    def test_list(self):
        result = as2_incoming_message.list()
        self.assert_returns(as2_incoming_message.list, result)
        self.assert_typed(result)

    def test_replay(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = as2_incoming_message.replay(id, params)
        self.assert_returns(as2_incoming_message.replay, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

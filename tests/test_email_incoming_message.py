import unittest
from tests.base import TestBase
from files_sdk import email_incoming_message


class EmailIncomingMessageTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = email_incoming_message.list()
        self.assert_returns(email_incoming_message.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

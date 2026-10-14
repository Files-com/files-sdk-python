import unittest
from tests.base import TestBase
from files_sdk import as2_outgoing_message


class As2OutgoingMessageTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = as2_outgoing_message.list()
        self.assert_returns(as2_outgoing_message.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

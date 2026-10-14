import unittest
from tests.base import TestBase
from files_sdk import outbound_connection_log


class OutboundConnectionLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = outbound_connection_log.list()
        self.assert_returns(outbound_connection_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

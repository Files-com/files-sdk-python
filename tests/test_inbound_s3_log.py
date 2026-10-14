import unittest
from tests.base import TestBase
from files_sdk import inbound_s3_log


class InboundS3LogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = inbound_s3_log.list()
        self.assert_returns(inbound_s3_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk import ftp_action_log


class FtpActionLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = ftp_action_log.list()
        self.assert_returns(ftp_action_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

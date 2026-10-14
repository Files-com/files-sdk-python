import unittest
from tests.base import TestBase
from files_sdk import sftp_action_log


class SftpActionLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = sftp_action_log.list()
        self.assert_returns(sftp_action_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

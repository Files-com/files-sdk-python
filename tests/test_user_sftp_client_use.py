import unittest
from tests.base import TestBase
from files_sdk import user_sftp_client_use


class UserSftpClientUseTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = user_sftp_client_use.list()
        self.assert_returns(user_sftp_client_use.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import UserSftpClientUse
from files_sdk import user_sftp_client_use

class UserSftpClientUseTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/user_sftp_client_uses"), "Mock path does not exist")
    def test_list(self):
        resp = user_sftp_client_use.list()

if __name__ == '__main__':
    unittest.main()
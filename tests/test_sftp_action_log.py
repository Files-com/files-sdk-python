import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SftpActionLog
from files_sdk import sftp_action_log

class SftpActionLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/sftp_action_logs"), "Mock path does not exist")
    def test_list(self):
        resp = sftp_action_log.list()

if __name__ == '__main__':
    unittest.main()
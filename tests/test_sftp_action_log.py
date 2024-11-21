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

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sftp_action_logs/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = sftp_action_log.create_export()

if __name__ == '__main__':
    unittest.main()
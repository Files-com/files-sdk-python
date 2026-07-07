import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import AutomationLog
from files_sdk import automation_log

class AutomationLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/automation_logs"), "Mock path does not exist")
    def test_list(self):
        resp = automation_log.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/automation_logs/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = automation_log.create_export()

if __name__ == '__main__':
    unittest.main()
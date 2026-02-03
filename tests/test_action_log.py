import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ActionLog
from files_sdk import action_log

class ActionLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/action_logs"), "Mock path does not exist")
    def test_list(self):
        resp = action_log.list()

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SyncLog
from files_sdk import sync_log

class SyncLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/sync_logs"), "Mock path does not exist")
    def test_list(self):
        resp = sync_log.list()

if __name__ == '__main__':
    unittest.main()
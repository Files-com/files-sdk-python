import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FileMigrationLog
from files_sdk import file_migration_log

class FileMigrationLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/file_migration_logs"), "Mock path does not exist")
    def test_list(self):
        resp = file_migration_log.list()

if __name__ == '__main__':
    unittest.main()
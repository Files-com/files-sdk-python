import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FileMigration
from files_sdk import file_migration

class FileMigrationTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/file_migrations/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        file_migration.find(id, params)

if __name__ == '__main__':
    unittest.main()
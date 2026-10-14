import unittest
from tests.base import TestBase
from files_sdk import file_migration_log


class FileMigrationLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = file_migration_log.list()
        self.assert_returns(file_migration_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

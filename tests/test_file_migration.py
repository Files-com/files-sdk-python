import unittest
from tests.base import TestBase
from files_sdk import file_migration


class FileMigrationTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = file_migration.find(id, params)
        self.assert_returns(file_migration.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

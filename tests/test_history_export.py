import unittest
from tests.base import TestBase
from files_sdk import history_export


class HistoryExportTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = history_export.find(id, params)
        self.assert_returns(history_export.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = history_export.create()
        self.assert_returns(history_export.create, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

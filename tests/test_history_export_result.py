import unittest
from tests.base import TestBase
from files_sdk import history_export_result


class HistoryExportResultTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        params = {
            "history_export_id": 12345,
        }
        result = history_export_result.list(params)
        self.assert_returns(history_export_result.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

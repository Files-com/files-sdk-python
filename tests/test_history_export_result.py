import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import HistoryExportResult
from files_sdk import history_export_result

class HistoryExportResultTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/history_export_results"), "Mock path does not exist")
    def test_list(self):
        params = {
            "history_export_id" : 12345,
        }
        history_export_result.list(params)

if __name__ == '__main__':
    unittest.main()
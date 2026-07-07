import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SyncApiUsageSnapshotReport
from files_sdk import sync_api_usage_snapshot_report

class SyncApiUsageSnapshotReportTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sync_api_usage_snapshot_reports"), "Mock path does not exist")
    def test_create(self):
        resp = sync_api_usage_snapshot_report.create()

if __name__ == '__main__':
    unittest.main()
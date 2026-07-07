import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import MonitoringStat
from files_sdk import monitoring_stat

class MonitoringStatTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/monitoring_stats"), "Mock path does not exist")
    def test_list(self):
        resp = monitoring_stat.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/monitoring_stats/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = monitoring_stat.create_export()

if __name__ == '__main__':
    unittest.main()
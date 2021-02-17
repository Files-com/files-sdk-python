import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import UsageSnapshot
from files_sdk import usage_snapshot

class UsageSnapshotTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/usage_snapshots"), "Mock path does not exist")
    def test_list(self):
        resp = usage_snapshot.list()

if __name__ == '__main__':
    unittest.main()
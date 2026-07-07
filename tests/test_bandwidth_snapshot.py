import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import BandwidthSnapshot
from files_sdk import bandwidth_snapshot

class BandwidthSnapshotTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bandwidth_snapshots"), "Mock path does not exist")
    def test_list(self):
        resp = bandwidth_snapshot.list()

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import RemoteBandwidthSnapshot
from files_sdk import remote_bandwidth_snapshot

class RemoteBandwidthSnapshotTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_bandwidth_snapshots"), "Mock path does not exist")
    def test_list(self):
        resp = remote_bandwidth_snapshot.list()

if __name__ == '__main__':
    unittest.main()
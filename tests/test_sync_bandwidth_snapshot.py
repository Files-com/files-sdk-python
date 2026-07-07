import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SyncBandwidthSnapshot
from files_sdk import sync_bandwidth_snapshot

class SyncBandwidthSnapshotTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sync_bandwidth_snapshots"), "Mock path does not exist")
    def test_create(self):
        params = {
            "remote_server_id" : 12345,
            "sync_bytes_sent" : 12345,
            "sync_bytes_received" : 12345,
        }
        sync_bandwidth_snapshot.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sync_bandwidth_snapshots/create_batch"), "Mock path does not exist")
    def test_create_batch(self):
        resp = sync_bandwidth_snapshot.create_batch()

if __name__ == '__main__':
    unittest.main()
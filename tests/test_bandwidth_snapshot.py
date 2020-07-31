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
    def test_list(self):
        resp = bandwidth_snapshot.list()

if __name__ == '__main__':
    unittest.main()
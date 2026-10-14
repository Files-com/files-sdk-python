import unittest
from tests.base import TestBase
from files_sdk import remote_bandwidth_snapshot


class RemoteBandwidthSnapshotTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = remote_bandwidth_snapshot.list()
        self.assert_returns(remote_bandwidth_snapshot.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

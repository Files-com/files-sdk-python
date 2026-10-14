import unittest
from tests.base import TestBase
from files_sdk import bandwidth_snapshot


class BandwidthSnapshotTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = bandwidth_snapshot.list()
        self.assert_returns(bandwidth_snapshot.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

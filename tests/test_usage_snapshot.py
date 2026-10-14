import unittest
from tests.base import TestBase
from files_sdk import usage_snapshot


class UsageSnapshotTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = usage_snapshot.list()
        self.assert_returns(usage_snapshot.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

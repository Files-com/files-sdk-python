import unittest
from tests.base import TestBase
from files_sdk import usage_daily_snapshot


class UsageDailySnapshotTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = usage_daily_snapshot.list()
        self.assert_returns(usage_daily_snapshot.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

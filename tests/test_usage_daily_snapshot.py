import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import UsageDailySnapshot
from files_sdk import usage_daily_snapshot

class UsageDailySnapshotTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        resp = usage_daily_snapshot.list()

if __name__ == '__main__':
    unittest.main()
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
    def test_list(self):
        resp = usage_snapshot.list()

if __name__ == '__main__':
    unittest.main()
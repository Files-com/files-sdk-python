import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import UsageSnapshot

class UsageSnapshotTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        resp = UsageSnapshot.do_list()

if __name__ == '__main__':
    unittest.main()
import unittest
from tests.base import TestBase
from files_sdk import sync_log


class SyncLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = sync_log.list()
        self.assert_returns(sync_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk import sync_run


class SyncRunTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = sync_run.list()
        self.assert_returns(sync_run.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sync_run.find(id, params)
        self.assert_returns(sync_run.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

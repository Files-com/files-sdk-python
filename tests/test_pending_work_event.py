import unittest
from tests.base import TestBase
from files_sdk import pending_work_event


class PendingWorkEventTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = pending_work_event.list()
        self.assert_returns(pending_work_event.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = pending_work_event.find(id, params)
        self.assert_returns(pending_work_event.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

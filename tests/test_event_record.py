import unittest
from tests.base import TestBase
from files_sdk import event_record


class EventRecordTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = event_record.list()
        self.assert_returns(event_record.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_record.find(id, params)
        self.assert_returns(event_record.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk import event_delivery_attempt


class EventDeliveryAttemptTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = event_delivery_attempt.list()
        self.assert_returns(event_delivery_attempt.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_delivery_attempt.find(id, params)
        self.assert_returns(event_delivery_attempt.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

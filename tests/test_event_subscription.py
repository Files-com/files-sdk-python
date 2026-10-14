import unittest
from tests.base import TestBase
from files_sdk.models import EventSubscription
from files_sdk import event_subscription


class EventSubscriptionTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        event_subscription = EventSubscription(params)
        result = event_subscription.update(params)
        self.assert_returns(EventSubscription.update, result)
        self.assert_typed(event_subscription)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        event_subscription = EventSubscription(params)
        event_subscription.delete(params)
        self.assert_typed(event_subscription)

    # Static Methods
    def test_list(self):
        result = event_subscription.list()
        self.assert_returns(event_subscription.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_subscription.find(id, params)
        self.assert_returns(event_subscription.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
        }
        result = event_subscription.create(params)
        self.assert_returns(event_subscription.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_subscription.update(id, params)
        self.assert_returns(event_subscription.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_subscription.delete(id, params)
        self.assert_returns(event_subscription.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

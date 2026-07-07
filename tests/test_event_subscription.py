import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import EventSubscription
from files_sdk import event_subscription

class EventSubscriptionTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/event_subscriptions/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        event_subscription = EventSubscription(params)
        event_subscription.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/event_subscriptions/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        event_subscription = EventSubscription(params)
        event_subscription.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_subscriptions"), "Mock path does not exist")
    def test_list(self):
        resp = event_subscription.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_subscriptions/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_subscription.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/event_subscriptions"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        event_subscription.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/event_subscriptions/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = event_subscription.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/event_subscriptions/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_subscription.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/event_subscriptions/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_subscription.delete(id, params)

if __name__ == '__main__':
    unittest.main()
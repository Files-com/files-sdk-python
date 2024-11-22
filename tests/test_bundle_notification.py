import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import BundleNotification
from files_sdk import bundle_notification

class BundleNotificationTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/bundle_notifications/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        bundle_notification = BundleNotification(params)
        bundle_notification.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/bundle_notifications/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        bundle_notification = BundleNotification(params)
        bundle_notification.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bundle_notifications"), "Mock path does not exist")
    def test_list(self):
        resp = bundle_notification.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bundle_notifications/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle_notification.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/bundle_notifications"), "Mock path does not exist")
    def test_create(self):
        params = {
            "bundle_id" : 12345,
        }
        bundle_notification.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/bundle_notifications/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle_notification.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/bundle_notifications/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle_notification.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Notification
from files_sdk import notification

class NotificationTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/notifications/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        notification = Notification(params)
        notification.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/notifications/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        notification = Notification(params)
        notification.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/notifications"), "Mock path does not exist")
    def test_list(self):
        resp = notification.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/notifications/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        notification.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/notifications"), "Mock path does not exist")
    def test_create(self):
        resp = notification.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/notifications/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        notification.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/notifications/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        notification.delete(id, params)

if __name__ == '__main__':
    unittest.main()
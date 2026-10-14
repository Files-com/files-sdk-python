import unittest
from tests.base import TestBase
from files_sdk.models import Notification
from files_sdk import notification


class NotificationTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        notification = Notification(params)
        result = notification.update(params)
        self.assert_returns(Notification.update, result)
        self.assert_typed(notification)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        notification = Notification(params)
        notification.delete(params)
        self.assert_typed(notification)

    # Static Methods
    def test_list(self):
        result = notification.list()
        self.assert_returns(notification.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = notification.find(id, params)
        self.assert_returns(notification.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = notification.create()
        self.assert_returns(notification.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = notification.update(id, params)
        self.assert_returns(notification.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = notification.delete(id, params)
        self.assert_returns(notification.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk.models import BundleNotification
from files_sdk import bundle_notification


class BundleNotificationTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        bundle_notification = BundleNotification(params)
        result = bundle_notification.update(params)
        self.assert_returns(BundleNotification.update, result)
        self.assert_typed(bundle_notification)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        bundle_notification = BundleNotification(params)
        bundle_notification.delete(params)
        self.assert_typed(bundle_notification)

    # Static Methods
    def test_list(self):
        result = bundle_notification.list()
        self.assert_returns(bundle_notification.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = bundle_notification.find(id, params)
        self.assert_returns(bundle_notification.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "bundle_id": 12345,
        }
        result = bundle_notification.create(params)
        self.assert_returns(bundle_notification.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = bundle_notification.update(id, params)
        self.assert_returns(bundle_notification.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = bundle_notification.delete(id, params)
        self.assert_returns(bundle_notification.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

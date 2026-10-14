import unittest
from tests.base import TestBase
from files_sdk import action_notification_export


class ActionNotificationExportTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = action_notification_export.find(id, params)
        self.assert_returns(action_notification_export.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = action_notification_export.create()
        self.assert_returns(action_notification_export.create, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

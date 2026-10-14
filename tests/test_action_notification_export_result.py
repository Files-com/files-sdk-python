import unittest
from tests.base import TestBase
from files_sdk import action_notification_export_result


class ActionNotificationExportResultTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        params = {
            "action_notification_export_id": 12345,
        }
        result = action_notification_export_result.list(params)
        self.assert_returns(action_notification_export_result.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

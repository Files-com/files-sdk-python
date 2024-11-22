import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ActionNotificationExportResult
from files_sdk import action_notification_export_result

class ActionNotificationExportResultTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/action_notification_export_results"), "Mock path does not exist")
    def test_list(self):
        params = {
            "action_notification_export_id" : 12345,
        }
        action_notification_export_result.list(params)

if __name__ == '__main__':
    unittest.main()
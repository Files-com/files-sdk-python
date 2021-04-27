import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ActionNotificationExport
from files_sdk import action_notification_export

class ActionNotificationExportTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/action_notification_exports/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        action_notification_export.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/action_notification_exports"), "Mock path does not exist")
    def test_create(self):
        resp = action_notification_export.create()

if __name__ == '__main__':
    unittest.main()
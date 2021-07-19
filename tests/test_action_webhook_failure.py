import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ActionWebhookFailure
from files_sdk import action_webhook_failure

class ActionWebhookFailureTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/action_webhook_failures/{id}/retry"), "Mock path does not exist")
    def test_retry(self):
        params = {
            "id" : 12345,
        }
        action_webhook_failure = ActionWebhookFailure(params)
        action_webhook_failure.retry(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/action_webhook_failures/{id}/retry"), "Mock path does not exist")
    def test_retry(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        action_webhook_failure.retry(id, params)

if __name__ == '__main__':
    unittest.main()
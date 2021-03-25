import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import WebhookTest
from files_sdk import webhook_test

class WebhookTestTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/webhook_tests"), "Mock path does not exist")
    def test_create(self):
        params = {
            "url" : "foo",
        }
        webhook_test.create(params)

if __name__ == '__main__':
    unittest.main()
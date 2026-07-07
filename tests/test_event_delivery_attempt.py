import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import EventDeliveryAttempt
from files_sdk import event_delivery_attempt

class EventDeliveryAttemptTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_delivery_attempts"), "Mock path does not exist")
    def test_list(self):
        resp = event_delivery_attempt.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_delivery_attempts/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_delivery_attempt.find(id, params)

if __name__ == '__main__':
    unittest.main()
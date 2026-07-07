import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import UserSecurityEvent
from files_sdk import user_security_event

class UserSecurityEventTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/user_security_events"), "Mock path does not exist")
    def test_list(self):
        resp = user_security_event.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/user_security_events/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user_security_event.find(id, params)

if __name__ == '__main__':
    unittest.main()
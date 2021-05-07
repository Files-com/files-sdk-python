import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ExternalEvent
from files_sdk import external_event

class ExternalEventTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/external_events"), "Mock path does not exist")
    def test_list(self):
        resp = external_event.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/external_events/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        external_event.find(id, params)

if __name__ == '__main__':
    unittest.main()
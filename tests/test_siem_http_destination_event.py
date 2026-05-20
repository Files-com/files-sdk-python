import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SiemHttpDestinationEvent
from files_sdk import siem_http_destination_event

class SiemHttpDestinationEventTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/siem_http_destination_events"), "Mock path does not exist")
    def test_list(self):
        resp = siem_http_destination_event.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/siem_http_destination_events/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        siem_http_destination_event.find(id, params)

if __name__ == '__main__':
    unittest.main()
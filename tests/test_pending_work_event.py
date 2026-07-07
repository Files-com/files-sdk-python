import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PendingWorkEvent
from files_sdk import pending_work_event

class PendingWorkEventTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/pending_work_events"), "Mock path does not exist")
    def test_list(self):
        resp = pending_work_event.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/pending_work_events/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        pending_work_event.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/pending_work_events/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = pending_work_event.create_export()

if __name__ == '__main__':
    unittest.main()
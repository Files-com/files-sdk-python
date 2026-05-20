import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import EventRecord
from files_sdk import event_record

class EventRecordTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_records"), "Mock path does not exist")
    def test_list(self):
        resp = event_record.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_records/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_record.find(id, params)

if __name__ == '__main__':
    unittest.main()
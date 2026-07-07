import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import EventTarget
from files_sdk import event_target

class EventTargetTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/event_targets/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        event_target = EventTarget(params)
        event_target.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/event_targets/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        event_target = EventTarget(params)
        event_target.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_targets"), "Mock path does not exist")
    def test_list(self):
        resp = event_target.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/event_targets/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_target.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/event_targets"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "target_type" : "foo",
            "config" : {},
        }
        event_target.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/event_targets/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = event_target.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/event_targets/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_target.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/event_targets/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        event_target.delete(id, params)

if __name__ == '__main__':
    unittest.main()
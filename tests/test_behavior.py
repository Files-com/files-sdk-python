import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Behavior
from files_sdk import behavior

class BehaviorTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/behaviors/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        behavior = Behavior(params)
        behavior.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/behaviors/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        behavior = Behavior(params)
        behavior.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/behaviors"), "Mock path does not exist")
    def test_list(self):
        resp = behavior.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/behaviors/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        behavior.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/behaviors/folders/{path}"), "Mock path does not exist")
    def test_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        behavior.list_for(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/behaviors"), "Mock path does not exist")
    def test_create(self):
        params = {
            "path" : "foo",
            "behavior" : "foo",
        }
        behavior.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/behaviors/webhook/test"), "Mock path does not exist")
    def test_webhook_test(self):
        params = {
            "url" : "foo",
        }
        behavior.webhook_test(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/behaviors/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        behavior.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/behaviors/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        behavior.delete(id, params)

if __name__ == '__main__':
    unittest.main()
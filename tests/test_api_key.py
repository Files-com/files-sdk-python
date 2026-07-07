import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ApiKey
from files_sdk import api_key

class ApiKeyTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/api_keys/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        api_key = ApiKey(params)
        api_key.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/api_keys/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        api_key = ApiKey(params)
        api_key.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/api_keys"), "Mock path does not exist")
    def test_list(self):
        resp = api_key.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/api_key"), "Mock path does not exist")
    def test_find_current(self):
        resp = api_key.find_current()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/api_keys/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        api_key.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/api_keys"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        api_key.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/api_key"), "Mock path does not exist")
    def test_update_current(self):
        resp = api_key.update_current()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/api_keys/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        api_key.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/api_key"), "Mock path does not exist")
    def test_delete_current(self):
        resp = api_key.delete_current()

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/api_keys/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        api_key.delete(id, params)

if __name__ == '__main__':
    unittest.main()
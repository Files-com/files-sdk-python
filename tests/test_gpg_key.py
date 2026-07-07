import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import GpgKey
from files_sdk import gpg_key

class GpgKeyTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/gpg_keys/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        gpg_key = GpgKey(params)
        gpg_key.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/gpg_keys/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        gpg_key = GpgKey(params)
        gpg_key.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/gpg_keys"), "Mock path does not exist")
    def test_list(self):
        resp = gpg_key.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/gpg_keys/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        gpg_key.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/gpg_keys"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        gpg_key.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/gpg_keys/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        gpg_key.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/gpg_keys/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        gpg_key.delete(id, params)

if __name__ == '__main__':
    unittest.main()
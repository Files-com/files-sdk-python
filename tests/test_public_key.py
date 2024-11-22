import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PublicKey
from files_sdk import public_key

class PublicKeyTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/public_keys/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
            "title" : "foo",
        }
        public_key = PublicKey(params)
        public_key.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/public_keys/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        public_key = PublicKey(params)
        public_key.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/public_keys"), "Mock path does not exist")
    def test_list(self):
        resp = public_key.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/public_keys/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        public_key.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/public_keys"), "Mock path does not exist")
    def test_create(self):
        params = {
            "title" : "foo",
            "public_key" : "foo",
        }
        public_key.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/public_keys/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "title" : "foo",
        }
        public_key.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/public_keys/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        public_key.delete(id, params)

if __name__ == '__main__':
    unittest.main()
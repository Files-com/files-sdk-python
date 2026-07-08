import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Secret
from files_sdk import secret

class SecretTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/secrets/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        secret = Secret(params)
        secret.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/secrets/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        secret = Secret(params)
        secret.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/secrets"), "Mock path does not exist")
    def test_list(self):
        resp = secret.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/secrets/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        secret.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/secrets"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "secret_type" : "foo",
        }
        secret.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/secrets/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        secret.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/secrets/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        secret.delete(id, params)

if __name__ == '__main__':
    unittest.main()
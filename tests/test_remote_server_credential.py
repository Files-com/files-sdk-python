import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import RemoteServerCredential
from files_sdk import remote_server_credential

class RemoteServerCredentialTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/remote_server_credentials/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        remote_server_credential = RemoteServerCredential(params)
        remote_server_credential.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/remote_server_credentials/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        remote_server_credential = RemoteServerCredential(params)
        remote_server_credential.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_server_credentials"), "Mock path does not exist")
    def test_list(self):
        resp = remote_server_credential.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_server_credentials/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server_credential.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_server_credentials"), "Mock path does not exist")
    def test_create(self):
        resp = remote_server_credential.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/remote_server_credentials/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server_credential.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/remote_server_credentials/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server_credential.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SftpHostKey
from files_sdk import sftp_host_key

class SftpHostKeyTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/sftp_host_keys/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        sftp_host_key = SftpHostKey(params)
        sftp_host_key.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/sftp_host_keys/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        sftp_host_key = SftpHostKey(params)
        sftp_host_key.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/sftp_host_keys"), "Mock path does not exist")
    def test_list(self):
        resp = sftp_host_key.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/sftp_host_keys/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sftp_host_key.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sftp_host_keys"), "Mock path does not exist")
    def test_create(self):
        resp = sftp_host_key.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/sftp_host_keys/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sftp_host_key.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/sftp_host_keys/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sftp_host_key.delete(id, params)

if __name__ == '__main__':
    unittest.main()
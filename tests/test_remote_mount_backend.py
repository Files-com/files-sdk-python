import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import RemoteMountBackend
from files_sdk import remote_mount_backend

class RemoteMountBackendTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_mount_backends/{id}/reset_status"), "Mock path does not exist")
    def test_reset_status(self):
        params = {
            "id" : 12345,
        }
        remote_mount_backend = RemoteMountBackend(params)
        remote_mount_backend.reset_status(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/remote_mount_backends/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        remote_mount_backend = RemoteMountBackend(params)
        remote_mount_backend.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/remote_mount_backends/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        remote_mount_backend = RemoteMountBackend(params)
        remote_mount_backend.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_mount_backends"), "Mock path does not exist")
    def test_list(self):
        resp = remote_mount_backend.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_mount_backends/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_mount_backend.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_mount_backends"), "Mock path does not exist")
    def test_create(self):
        params = {
            "canary_file_path" : "foo",
            "remote_server_mount_id" : 12345,
            "remote_server_id" : 12345,
        }
        remote_mount_backend.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_mount_backends/{id}/reset_status"), "Mock path does not exist")
    def test_reset_status(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_mount_backend.reset_status(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/remote_mount_backends/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_mount_backend.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/remote_mount_backends/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_mount_backend.delete(id, params)

if __name__ == '__main__':
    unittest.main()
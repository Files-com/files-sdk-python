import unittest
from tests.base import TestBase
from files_sdk.models import RemoteMountBackend
from files_sdk import remote_mount_backend


class RemoteMountBackendTest(TestBase):
    # Instance Methods
    def test_instance_reset_status(self):
        params = {
            "id": 12345,
        }
        remote_mount_backend = RemoteMountBackend(params)
        remote_mount_backend.reset_status(params)
        self.assert_typed(remote_mount_backend)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        remote_mount_backend = RemoteMountBackend(params)
        result = remote_mount_backend.update(params)
        self.assert_returns(RemoteMountBackend.update, result)
        self.assert_typed(remote_mount_backend)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        remote_mount_backend = RemoteMountBackend(params)
        remote_mount_backend.delete(params)
        self.assert_typed(remote_mount_backend)

    # Static Methods
    def test_list(self):
        result = remote_mount_backend.list()
        self.assert_returns(remote_mount_backend.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_mount_backend.find(id, params)
        self.assert_returns(remote_mount_backend.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "canary_file_path": "foo",
            "remote_server_mount_id": 12345,
            "remote_server_id": 12345,
        }
        result = remote_mount_backend.create(params)
        self.assert_returns(remote_mount_backend.create, result)
        self.assert_typed(result)

    def test_reset_status(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_mount_backend.reset_status(id, params)
        self.assert_returns(remote_mount_backend.reset_status, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_mount_backend.update(id, params)
        self.assert_returns(remote_mount_backend.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_mount_backend.delete(id, params)
        self.assert_returns(remote_mount_backend.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

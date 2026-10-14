import unittest
from tests.base import TestBase
from files_sdk.models import RemoteServerCredential
from files_sdk import remote_server_credential


class RemoteServerCredentialTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        remote_server_credential = RemoteServerCredential(params)
        result = remote_server_credential.update(params)
        self.assert_returns(RemoteServerCredential.update, result)
        self.assert_typed(remote_server_credential)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        remote_server_credential = RemoteServerCredential(params)
        remote_server_credential.delete(params)
        self.assert_typed(remote_server_credential)

    # Static Methods
    def test_list(self):
        result = remote_server_credential.list()
        self.assert_returns(remote_server_credential.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server_credential.find(id, params)
        self.assert_returns(remote_server_credential.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = remote_server_credential.create()
        self.assert_returns(remote_server_credential.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server_credential.update(id, params)
        self.assert_returns(remote_server_credential.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server_credential.delete(id, params)
        self.assert_returns(remote_server_credential.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

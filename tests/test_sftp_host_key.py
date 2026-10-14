import unittest
from tests.base import TestBase
from files_sdk.models import SftpHostKey
from files_sdk import sftp_host_key


class SftpHostKeyTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        sftp_host_key = SftpHostKey(params)
        result = sftp_host_key.update(params)
        self.assert_returns(SftpHostKey.update, result)
        self.assert_typed(sftp_host_key)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        sftp_host_key = SftpHostKey(params)
        sftp_host_key.delete(params)
        self.assert_typed(sftp_host_key)

    # Static Methods
    def test_list(self):
        result = sftp_host_key.list()
        self.assert_returns(sftp_host_key.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sftp_host_key.find(id, params)
        self.assert_returns(sftp_host_key.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = sftp_host_key.create()
        self.assert_returns(sftp_host_key.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sftp_host_key.update(id, params)
        self.assert_returns(sftp_host_key.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sftp_host_key.delete(id, params)
        self.assert_returns(sftp_host_key.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

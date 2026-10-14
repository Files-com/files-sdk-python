import unittest
from tests.base import TestBase
from files_sdk.models import GpgKey
from files_sdk import gpg_key


class GpgKeyTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        gpg_key = GpgKey(params)
        result = gpg_key.update(params)
        self.assert_returns(GpgKey.update, result)
        self.assert_typed(gpg_key)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        gpg_key = GpgKey(params)
        gpg_key.delete(params)
        self.assert_typed(gpg_key)

    # Static Methods
    def test_list(self):
        result = gpg_key.list()
        self.assert_returns(gpg_key.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = gpg_key.find(id, params)
        self.assert_returns(gpg_key.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
        }
        result = gpg_key.create(params)
        self.assert_returns(gpg_key.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = gpg_key.update(id, params)
        self.assert_returns(gpg_key.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = gpg_key.delete(id, params)
        self.assert_returns(gpg_key.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

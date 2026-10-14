import unittest
from tests.base import TestBase
from files_sdk.models import Secret
from files_sdk import secret


class SecretTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        secret = Secret(params)
        result = secret.update(params)
        self.assert_returns(Secret.update, result)
        self.assert_typed(secret)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        secret = Secret(params)
        secret.delete(params)
        self.assert_typed(secret)

    # Static Methods
    def test_list(self):
        result = secret.list()
        self.assert_returns(secret.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = secret.find(id, params)
        self.assert_returns(secret.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "secret_type": "foo",
        }
        result = secret.create(params)
        self.assert_returns(secret.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = secret.update(id, params)
        self.assert_returns(secret.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = secret.delete(id, params)
        self.assert_returns(secret.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk.models import PublicKey
from files_sdk import public_key


class PublicKeyTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
            "title": "foo",
        }
        public_key = PublicKey(params)
        result = public_key.update(params)
        self.assert_returns(PublicKey.update, result)
        self.assert_typed(public_key)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        public_key = PublicKey(params)
        public_key.delete(params)
        self.assert_typed(public_key)

    # Static Methods
    def test_list(self):
        result = public_key.list()
        self.assert_returns(public_key.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = public_key.find(id, params)
        self.assert_returns(public_key.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "title": "foo",
        }
        result = public_key.create(params)
        self.assert_returns(public_key.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
            "title": "foo",
        }
        result = public_key.update(id, params)
        self.assert_returns(public_key.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = public_key.delete(id, params)
        self.assert_returns(public_key.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

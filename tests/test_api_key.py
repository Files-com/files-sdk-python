import unittest
from tests.base import TestBase
from files_sdk.models import ApiKey
from files_sdk import api_key


class ApiKeyTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        api_key = ApiKey(params)
        result = api_key.update(params)
        self.assert_returns(ApiKey.update, result)
        self.assert_typed(api_key)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        api_key = ApiKey(params)
        api_key.delete(params)
        self.assert_typed(api_key)

    # Static Methods
    def test_list(self):
        result = api_key.list()
        self.assert_returns(api_key.list, result)
        self.assert_typed(result)

    def test_find_current(self):
        result = api_key.find_current()
        self.assert_returns(api_key.find_current, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = api_key.find(id, params)
        self.assert_returns(api_key.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
        }
        result = api_key.create(params)
        self.assert_returns(api_key.create, result)
        self.assert_typed(result)

    def test_update_current(self):
        result = api_key.update_current()
        self.assert_returns(api_key.update_current, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = api_key.update(id, params)
        self.assert_returns(api_key.update, result)
        self.assert_typed(result)

    def test_delete_current(self):
        result = api_key.delete_current()
        self.assert_returns(api_key.delete_current, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = api_key.delete(id, params)
        self.assert_returns(api_key.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ApiKey
from files_sdk import api_key

class ApiKeyTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
        }
        api_key = ApiKey(params)
        api_key.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        api_key = ApiKey(params)
        api_key.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = api_key.list()

    def test_find_current(self):
        resp = api_key.find_current()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        api_key.find(id, params)

    def test_create(self):
        resp = api_key.create()

    def test_update_current(self):
        resp = api_key.update_current()

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        api_key.update(id, params)

    def test_current(self):
        resp = api_key.current()

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        api_key.delete(id, params)

if __name__ == '__main__':
    unittest.main()
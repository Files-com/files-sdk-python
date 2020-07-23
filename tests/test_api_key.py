import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import ApiKey

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
    def test_do_list(self):
        resp = ApiKey.do_list()

    def test_do_find_current(self):
        resp = ApiKey.do_find_current()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ApiKey.do_find(id, params)

    def test_do_create(self):
        resp = ApiKey.do_create()

    def test_do_update_current(self):
        resp = ApiKey.do_update_current()

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ApiKey.do_update(id, params)

    def test_do_delete_current(self):
        resp = ApiKey.do_delete_current()

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ApiKey.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
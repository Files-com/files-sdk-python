import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import As2Key
from files_sdk import as2_key

class As2KeyTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "as2_partnership_name" : "foo",
        }
        as2_key = As2Key(params)
        as2_key.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        as2_key = As2Key(params)
        as2_key.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = as2_key.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        as2_key.find(id, params)

    def test_create(self):
        params = {
            "as2_partnership_name" : "foo",
            "public_key" : "foo",
        }
        as2_key.create(params)

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "as2_partnership_name" : "foo",
        }
        as2_key.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        as2_key.delete(id, params)

if __name__ == '__main__':
    unittest.main()
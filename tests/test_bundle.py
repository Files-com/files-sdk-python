import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Bundle
from files_sdk import bundle

class BundleTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
        }
        bundle = Bundle(params)
        bundle.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        bundle = Bundle(params)
        bundle.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = bundle.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle.find(id, params)



    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Request
from files_sdk import request

class RequestTest(TestBase):
    pass 
    # Instance Methods
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        request = Request(params)
        request.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = request.list()

    def test_get_folder(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        request.get_folder(path, params)

    def test_create(self):
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        request.create(params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        request.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Request
from files_sdk import request

class RequestTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        path = "foo"
        resp = request.list(path, )

    def test_find_folder(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        request.find_folder(path, params)

    def test_create(self):
        path = "foo"
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        request.create(path, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        request.delete(id, params)

if __name__ == '__main__':
    unittest.main()
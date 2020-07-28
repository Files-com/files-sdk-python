import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import UserRequest
from files_sdk import user_request

class UserRequestTest(TestBase):
    pass 
    # Instance Methods
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        user_request = UserRequest(params)
        user_request.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = user_request.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user_request.find(id, params)

    def test_create(self):
        params = {
            "name" : "foo",
            "email" : "foo",
            "details" : "foo",
        }
        user_request.create(params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user_request.delete(id, params)

if __name__ == '__main__':
    unittest.main()
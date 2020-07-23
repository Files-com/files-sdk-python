import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import UserRequest

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
    def test_do_list(self):
        resp = UserRequest.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        UserRequest.do_find(id, params)

    def test_do_create(self):
        params = {
            "name" : "foo",
            "email" : "foo",
            "details" : "foo",
        }
        UserRequest.do_create(params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        UserRequest.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
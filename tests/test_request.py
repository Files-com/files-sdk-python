import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Request

class RequestTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        path = "foo"
        resp = Request.do_list(path, )

    def test_do_find_folder(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        Request.do_find_folder(path, params)

    def test_do_create(self):
        path = "foo"
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        Request.do_create(path, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Request.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
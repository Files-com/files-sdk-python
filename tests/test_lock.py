import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Lock

class LockTest(TestBase):
    pass 
    # Instance Methods
    def test_delete(self):
        params = {
            "path" : "foo",
            "token" : "foo",
        }
        lock = Lock(params)
        lock.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        Lock.do_list_for(path, params)

    def test_do_create(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        Lock.do_create(path, params)

    def test_do_delete(self):
        path = "foo"
        params = {
            "path" : "foo",
            "token" : "foo",
        }
        Lock.do_delete(path, params)

if __name__ == '__main__':
    unittest.main()
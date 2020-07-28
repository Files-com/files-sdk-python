import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Lock
from files_sdk import lock

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
    def test_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        lock.list_for(path, params)

    def test_create(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        lock.create(path, params)

    def test_delete(self):
        path = "foo"
        params = {
            "path" : "foo",
            "token" : "foo",
        }
        lock.delete(path, params)

if __name__ == '__main__':
    unittest.main()
import unittest
from tests.base import TestBase
from files_sdk.models import Lock
from files_sdk import lock


class LockTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "path": "foo",
            "token": "foo",
        }
        lock = Lock(params)
        lock.delete(params)
        self.assert_typed(lock)

    # Static Methods
    def test_list_for(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = lock.list_for(path, params)
        self.assert_returns(lock.list_for, result)
        self.assert_typed(result)

    def test_create(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = lock.create(path, params)
        self.assert_returns(lock.create, result)
        self.assert_typed(result)

    def test_delete(self):
        path = "foo"
        params = {
            "path": "foo",
            "token": "foo",
        }
        result = lock.delete(path, params)
        self.assert_returns(lock.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

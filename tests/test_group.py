import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Group
from files_sdk import group

class GroupTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
        }
        group = Group(params)
        group.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        group = Group(params)
        group.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = group.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        group.find(id, params)

    def test_create(self):
        resp = group.create()

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        group.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        group.delete(id, params)

if __name__ == '__main__':
    unittest.main()
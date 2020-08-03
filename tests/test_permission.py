import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Permission
from files_sdk import permission

class PermissionTest(TestBase):
    pass 
    # Instance Methods
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        permission = Permission(params)
        permission.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = permission.list()

    def test_create(self):
        resp = permission.create()

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        permission.delete(id, params)

if __name__ == '__main__':
    unittest.main()
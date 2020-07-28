import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Permission
from files_sdk import permission

class PermissionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        path = "foo"
        resp = permission.list(path, )

    def test_create(self):
        path = "foo"
        resp = permission.create(path, )

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        permission.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Permission

class PermissionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        path = "foo"
        resp = Permission.do_list(path, )

    def test_do_create(self):
        path = "foo"
        resp = Permission.do_create(path, )

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Permission.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
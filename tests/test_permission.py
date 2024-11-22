import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Permission
from files_sdk import permission

class PermissionTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/permissions/{id}"), "Mock path does not exist")
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
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/permissions"), "Mock path does not exist")
    def test_list(self):
        resp = permission.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/permissions"), "Mock path does not exist")
    def test_create(self):
        params = {
            "path" : "foo",
        }
        permission.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/permissions/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        permission.delete(id, params)

if __name__ == '__main__':
    unittest.main()
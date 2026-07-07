import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Group
from files_sdk import group

class GroupTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/groups/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        group = Group(params)
        group.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/groups/{id}"), "Mock path does not exist")
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
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/groups"), "Mock path does not exist")
    def test_list(self):
        resp = group.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/groups/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        group.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/groups"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        group.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/groups/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        group.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/groups/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        group.delete(id, params)

if __name__ == '__main__':
    unittest.main()
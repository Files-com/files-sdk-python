import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import GroupUser
from files_sdk import group_user

class GroupUserTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/group_users/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
            "group_id" : 12345,
            "user_id" : 12345,
        }
        group_user = GroupUser(params)
        group_user.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/group_users/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
            "group_id" : 12345,
            "user_id" : 12345,
        }
        group_user = GroupUser(params)
        group_user.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/group_users"), "Mock path does not exist")
    def test_list(self):
        resp = group_user.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/group_users"), "Mock path does not exist")
    def test_create(self):
        params = {
            "group_id" : 12345,
            "user_id" : 12345,
        }
        group_user.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/group_users/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "group_id" : 12345,
            "user_id" : 12345,
        }
        group_user.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/group_users/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
            "group_id" : 12345,
            "user_id" : 12345,
        }
        group_user.delete(id, params)

if __name__ == '__main__':
    unittest.main()
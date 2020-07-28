import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import GroupUser
from files_sdk import group_user

class GroupUserTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "group_id" : 12345,
            "user_id" : 12345,
        }
        group_user = GroupUser(params)
        group_user.update(params)

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
    def test_list(self):
        resp = group_user.list()

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "group_id" : 12345,
            "user_id" : 12345,
        }
        group_user.update(id, params)

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
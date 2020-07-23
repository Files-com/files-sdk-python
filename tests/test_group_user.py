import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import GroupUser

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
    def test_do_list(self):
        resp = GroupUser.do_list()

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "group_id" : 12345,
            "user_id" : 12345,
        }
        GroupUser.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
            "group_id" : 12345,
            "user_id" : 12345,
        }
        GroupUser.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
from tests.base import TestBase
from files_sdk.models import GroupUser
from files_sdk import group_user


class GroupUserTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
            "group_id": 12345,
            "user_id": 12345,
        }
        group_user = GroupUser(params)
        result = group_user.update(params)
        self.assert_returns(GroupUser.update, result)
        self.assert_typed(group_user)

    def test_instance_delete(self):
        params = {
            "id": 12345,
            "group_id": 12345,
            "user_id": 12345,
        }
        group_user = GroupUser(params)
        group_user.delete(params)
        self.assert_typed(group_user)

    # Static Methods
    def test_list(self):
        result = group_user.list()
        self.assert_returns(group_user.list, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "group_id": 12345,
            "user_id": 12345,
        }
        result = group_user.create(params)
        self.assert_returns(group_user.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
            "group_id": 12345,
            "user_id": 12345,
        }
        result = group_user.update(id, params)
        self.assert_returns(group_user.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
            "group_id": 12345,
            "user_id": 12345,
        }
        result = group_user.delete(id, params)
        self.assert_returns(group_user.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

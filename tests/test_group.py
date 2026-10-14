import unittest
from tests.base import TestBase
from files_sdk.models import Group
from files_sdk import group


class GroupTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        group = Group(params)
        result = group.update(params)
        self.assert_returns(Group.update, result)
        self.assert_typed(group)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        group = Group(params)
        group.delete(params)
        self.assert_typed(group)

    # Static Methods
    def test_list(self):
        result = group.list()
        self.assert_returns(group.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = group.find(id, params)
        self.assert_returns(group.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
        }
        result = group.create(params)
        self.assert_returns(group.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = group.update(id, params)
        self.assert_returns(group.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = group.delete(id, params)
        self.assert_returns(group.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

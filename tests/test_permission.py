import unittest
from tests.base import TestBase
from files_sdk.models import Permission
from files_sdk import permission


class PermissionTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        permission = Permission(params)
        permission.delete(params)
        self.assert_typed(permission)

    # Static Methods
    def test_list(self):
        result = permission.list()
        self.assert_returns(permission.list, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "path": "foo",
        }
        result = permission.create(params)
        self.assert_returns(permission.create, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = permission.delete(id, params)
        self.assert_returns(permission.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

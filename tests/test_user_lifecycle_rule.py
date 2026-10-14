import unittest
from tests.base import TestBase
from files_sdk.models import UserLifecycleRule
from files_sdk import user_lifecycle_rule


class UserLifecycleRuleTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        user_lifecycle_rule = UserLifecycleRule(params)
        result = user_lifecycle_rule.update(params)
        self.assert_returns(UserLifecycleRule.update, result)
        self.assert_typed(user_lifecycle_rule)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        user_lifecycle_rule = UserLifecycleRule(params)
        user_lifecycle_rule.delete(params)
        self.assert_typed(user_lifecycle_rule)

    # Static Methods
    def test_list(self):
        result = user_lifecycle_rule.list()
        self.assert_returns(user_lifecycle_rule.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_lifecycle_rule.find(id, params)
        self.assert_returns(user_lifecycle_rule.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = user_lifecycle_rule.create()
        self.assert_returns(user_lifecycle_rule.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_lifecycle_rule.update(id, params)
        self.assert_returns(user_lifecycle_rule.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_lifecycle_rule.delete(id, params)
        self.assert_returns(user_lifecycle_rule.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

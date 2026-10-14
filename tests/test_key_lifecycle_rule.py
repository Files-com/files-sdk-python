import unittest
from tests.base import TestBase
from files_sdk.models import KeyLifecycleRule
from files_sdk import key_lifecycle_rule


class KeyLifecycleRuleTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        key_lifecycle_rule = KeyLifecycleRule(params)
        result = key_lifecycle_rule.update(params)
        self.assert_returns(KeyLifecycleRule.update, result)
        self.assert_typed(key_lifecycle_rule)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        key_lifecycle_rule = KeyLifecycleRule(params)
        key_lifecycle_rule.delete(params)
        self.assert_typed(key_lifecycle_rule)

    # Static Methods
    def test_list(self):
        result = key_lifecycle_rule.list()
        self.assert_returns(key_lifecycle_rule.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = key_lifecycle_rule.find(id, params)
        self.assert_returns(key_lifecycle_rule.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = key_lifecycle_rule.create()
        self.assert_returns(key_lifecycle_rule.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = key_lifecycle_rule.update(id, params)
        self.assert_returns(key_lifecycle_rule.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = key_lifecycle_rule.delete(id, params)
        self.assert_returns(key_lifecycle_rule.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

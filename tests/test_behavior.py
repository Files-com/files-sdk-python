import unittest
from tests.base import TestBase
from files_sdk.models import Behavior
from files_sdk import behavior


class BehaviorTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        behavior = Behavior(params)
        result = behavior.update(params)
        self.assert_returns(Behavior.update, result)
        self.assert_typed(behavior)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        behavior = Behavior(params)
        behavior.delete(params)
        self.assert_typed(behavior)

    # Static Methods
    def test_list(self):
        result = behavior.list()
        self.assert_returns(behavior.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = behavior.find(id, params)
        self.assert_returns(behavior.find, result)
        self.assert_typed(result)

    def test_list_for(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = behavior.list_for(path, params)
        self.assert_returns(behavior.list_for, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "path": "foo",
            "behavior": "foo",
        }
        result = behavior.create(params)
        self.assert_returns(behavior.create, result)
        self.assert_typed(result)

    def test_webhook_test(self):
        params = {
            "url": "foo",
        }
        result = behavior.webhook_test(params)
        self.assert_returns(behavior.webhook_test, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = behavior.update(id, params)
        self.assert_returns(behavior.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = behavior.delete(id, params)
        self.assert_returns(behavior.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

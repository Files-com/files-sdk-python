import unittest
from tests.base import TestBase
from files_sdk.models import Automation
from files_sdk import automation


class AutomationTest(TestBase):
    # Instance Methods
    def test_instance_upgrade(self):
        params = {
            "id": 12345,
        }
        automation = Automation(params)
        result = automation.upgrade(params)
        self.assert_returns(Automation.upgrade, result)
        self.assert_typed(automation)

    def test_instance_manual_run(self):
        params = {
            "id": 12345,
        }
        automation = Automation(params)
        automation.manual_run(params)
        self.assert_typed(automation)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        automation = Automation(params)
        result = automation.update(params)
        self.assert_returns(Automation.update, result)
        self.assert_typed(automation)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        automation = Automation(params)
        automation.delete(params)
        self.assert_typed(automation)

    # Static Methods
    def test_list(self):
        result = automation.list()
        self.assert_returns(automation.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation.find(id, params)
        self.assert_returns(automation.find, result)
        self.assert_typed(result)

    def test_get_authoring_schema(self):
        result = automation.get_authoring_schema()
        self.assert_returns(automation.get_authoring_schema, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "automation": "foo",
        }
        result = automation.create(params)
        self.assert_returns(automation.create, result)
        self.assert_typed(result)

    def test_upgrade(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation.upgrade(id, params)
        self.assert_returns(automation.upgrade, result)
        self.assert_typed(result)

    def test_manual_run(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation.manual_run(id, params)
        self.assert_returns(automation.manual_run, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation.update(id, params)
        self.assert_returns(automation.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation.delete(id, params)
        self.assert_returns(automation.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

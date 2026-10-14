import unittest
from tests.base import TestBase
from files_sdk.models import AutomationRun
from files_sdk import automation_run


class AutomationRunTest(TestBase):
    # Instance Methods
    def test_instance_cancel(self):
        params = {
            "id": 12345,
        }
        automation_run = AutomationRun(params)
        result = automation_run.cancel(params)
        self.assert_returns(AutomationRun.cancel, result)
        self.assert_typed(automation_run)

    def test_instance_rerun(self):
        params = {
            "id": 12345,
            "node_id": "foo",
        }
        automation_run = AutomationRun(params)
        result = automation_run.rerun(params)
        self.assert_returns(AutomationRun.rerun, result)
        self.assert_typed(automation_run)

    # Static Methods
    def test_list(self):
        params = {
            "automation_id": 12345,
        }
        result = automation_run.list(params)
        self.assert_returns(automation_run.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation_run.find(id, params)
        self.assert_returns(automation_run.find, result)
        self.assert_typed(result)

    def test_find_node(self):
        id = 12345
        params = {
            "id": 12345,
            "node_id": "foo",
        }
        result = automation_run.find_node(id, params)
        self.assert_returns(automation_run.find_node, result)
        self.assert_typed(result)

    def test_cancel(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation_run.cancel(id, params)
        self.assert_returns(automation_run.cancel, result)
        self.assert_typed(result)

    def test_rerun(self):
        id = 12345
        params = {
            "id": 12345,
            "node_id": "foo",
        }
        result = automation_run.rerun(id, params)
        self.assert_returns(automation_run.rerun, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

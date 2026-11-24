import unittest
from tests.base import TestBase
from files_sdk.models import AutomationVersion
from files_sdk import automation_version


class AutomationVersionTest(TestBase):
    # Instance Methods
    def test_instance_restore(self):
        params = {
            "id": 12345,
        }
        automation_version = AutomationVersion(params)
        result = automation_version.restore(params)
        self.assert_returns(AutomationVersion.restore, result)
        self.assert_typed(automation_version)

    # Static Methods
    def test_list(self):
        params = {
            "automation_id": 12345,
        }
        result = automation_version.list(params)
        self.assert_returns(automation_version.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation_version.find(id, params)
        self.assert_returns(automation_version.find, result)
        self.assert_typed(result)

    def test_restore(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = automation_version.restore(id, params)
        self.assert_returns(automation_version.restore, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

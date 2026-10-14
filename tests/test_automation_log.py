import unittest
from tests.base import TestBase
from files_sdk import automation_log


class AutomationLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = automation_log.list()
        self.assert_returns(automation_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

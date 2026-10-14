import unittest
from tests.base import TestBase
from files_sdk import action_log


class ActionLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = action_log.list()
        self.assert_returns(action_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

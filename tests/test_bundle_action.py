import unittest
from tests.base import TestBase
from files_sdk import bundle_action


class BundleActionTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = bundle_action.list()
        self.assert_returns(bundle_action.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

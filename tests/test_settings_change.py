import unittest
from tests.base import TestBase
from files_sdk import settings_change


class SettingsChangeTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = settings_change.list()
        self.assert_returns(settings_change.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

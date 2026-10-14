import unittest
from tests.base import TestBase
from files_sdk import inbox_registration


class InboxRegistrationTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = inbox_registration.list()
        self.assert_returns(inbox_registration.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

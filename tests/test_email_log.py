import unittest
from tests.base import TestBase
from files_sdk import email_log


class EmailLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = email_log.list()
        self.assert_returns(email_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

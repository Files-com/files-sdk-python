import unittest
from tests.base import TestBase
from files_sdk import api_request_log


class ApiRequestLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = api_request_log.list()
        self.assert_returns(api_request_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

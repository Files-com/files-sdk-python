import unittest
from tests.base import TestBase
from files_sdk import exavault_api_request_log


class ExavaultApiRequestLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = exavault_api_request_log.list()
        self.assert_returns(exavault_api_request_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

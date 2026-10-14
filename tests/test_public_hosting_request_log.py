import unittest
from tests.base import TestBase
from files_sdk import public_hosting_request_log


class PublicHostingRequestLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = public_hosting_request_log.list()
        self.assert_returns(public_hosting_request_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

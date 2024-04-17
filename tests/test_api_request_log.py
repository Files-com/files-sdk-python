import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ApiRequestLog
from files_sdk import api_request_log

class ApiRequestLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/api_request_logs"), "Mock path does not exist")
    def test_list(self):
        resp = api_request_log.list()

if __name__ == '__main__':
    unittest.main()
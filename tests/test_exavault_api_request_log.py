import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ExavaultApiRequestLog
from files_sdk import exavault_api_request_log

class ExavaultApiRequestLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/exavault_api_request_logs"), "Mock path does not exist")
    def test_list(self):
        resp = exavault_api_request_log.list()

if __name__ == '__main__':
    unittest.main()
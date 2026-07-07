import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PublicHostingRequestLog
from files_sdk import public_hosting_request_log

class PublicHostingRequestLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/public_hosting_request_logs"), "Mock path does not exist")
    def test_list(self):
        resp = public_hosting_request_log.list()

if __name__ == '__main__':
    unittest.main()
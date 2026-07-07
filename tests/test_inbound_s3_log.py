import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import InboundS3Log
from files_sdk import inbound_s3_log

class InboundS3LogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/inbound_s3_logs"), "Mock path does not exist")
    def test_list(self):
        resp = inbound_s3_log.list()

if __name__ == '__main__':
    unittest.main()
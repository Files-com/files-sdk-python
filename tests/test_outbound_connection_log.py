import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import OutboundConnectionLog
from files_sdk import outbound_connection_log

class OutboundConnectionLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/outbound_connection_logs"), "Mock path does not exist")
    def test_list(self):
        resp = outbound_connection_log.list()

if __name__ == '__main__':
    unittest.main()
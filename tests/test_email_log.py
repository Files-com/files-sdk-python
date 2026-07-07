import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import EmailLog
from files_sdk import email_log

class EmailLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/email_logs"), "Mock path does not exist")
    def test_list(self):
        resp = email_log.list()

if __name__ == '__main__':
    unittest.main()
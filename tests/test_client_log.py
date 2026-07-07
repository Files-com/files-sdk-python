import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ClientLog
from files_sdk import client_log

class ClientLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/client_logs/log"), "Mock path does not exist")
    def test_log(self):
        params = {
            "identifier" : "foo",
            "body" : "foo",
        }
        client_log.log(params)

if __name__ == '__main__':
    unittest.main()
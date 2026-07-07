import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FrontEndServer
from files_sdk import front_end_server

class FrontEndServerTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/front_end_servers"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        front_end_server.create(params)

if __name__ == '__main__':
    unittest.main()
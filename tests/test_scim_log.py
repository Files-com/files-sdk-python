import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ScimLog
from files_sdk import scim_log

class ScimLogTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/scim_logs"), "Mock path does not exist")
    def test_list(self):
        resp = scim_log.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/scim_logs/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        scim_log.find(id, params)

if __name__ == '__main__':
    unittest.main()
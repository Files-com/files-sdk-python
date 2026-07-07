import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import AutomationRun
from files_sdk import automation_run

class AutomationRunTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/automation_runs"), "Mock path does not exist")
    def test_list(self):
        params = {
            "automation_id" : 12345,
        }
        automation_run.list(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/automation_runs/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation_run.find(id, params)

if __name__ == '__main__':
    unittest.main()
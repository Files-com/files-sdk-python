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

if __name__ == '__main__':
    unittest.main()
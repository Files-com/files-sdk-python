import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Plan
from files_sdk import plan

class PlanTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/plans"), "Mock path does not exist")
    def test_list(self):
        resp = plan.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/plans/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = plan.create_export()

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import BundleAction
from files_sdk import bundle_action

class BundleActionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bundle_actions"), "Mock path does not exist")
    def test_list(self):
        resp = bundle_action.list()

if __name__ == '__main__':
    unittest.main()
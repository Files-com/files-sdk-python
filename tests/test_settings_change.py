import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SettingsChange
from files_sdk import settings_change

class SettingsChangeTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/settings_changes"), "Mock path does not exist")
    def test_list(self):
        resp = settings_change.list()

if __name__ == '__main__':
    unittest.main()
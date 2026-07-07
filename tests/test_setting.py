import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Setting
from files_sdk import setting

class SettingTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/settings/languages"), "Mock path does not exist")
    def test_languages(self):
        resp = setting.languages()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/settings"), "Mock path does not exist")
    def test_list(self):
        resp = setting.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/settings/domain"), "Mock path does not exist")
    def test_get_domain(self):
        params = {
            "domain" : "foo",
        }
        setting.get_domain(params)

if __name__ == '__main__':
    unittest.main()
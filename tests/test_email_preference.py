import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import EmailPreference
from files_sdk import email_preference

class EmailPreferenceTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/email_preferences/{token}"), "Mock path does not exist")
    def test_get(self):
        token = "foo"
        params = {
            "token" : "foo",
        }
        email_preference.get(token, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/email_preferences/{token}"), "Mock path does not exist")
    def test_update(self):
        token = "foo"
        params = {
            "token" : "foo",
        }
        email_preference.update(token, params)

if __name__ == '__main__':
    unittest.main()
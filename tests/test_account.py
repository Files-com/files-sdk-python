import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Account
from files_sdk import account

class AccountTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/account"), "Mock path does not exist")
    def test_get(self):
        resp = account.get()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/account"), "Mock path does not exist")
    def test_create(self):
        resp = account.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/account"), "Mock path does not exist")
    def test_update(self):
        resp = account.update()

if __name__ == '__main__':
    unittest.main()
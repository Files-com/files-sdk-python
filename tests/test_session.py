import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Session
from files_sdk import session

class SessionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions"), "Mock path does not exist")
    def test_create(self):
        resp = session.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/sessions"), "Mock path does not exist")
    def test_delete(self):
        resp = session.delete()

if __name__ == '__main__':
    unittest.main()
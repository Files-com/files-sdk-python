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
    def test_create(self):
        resp = session.create()

    def test_delete(self):
        resp = session.delete()

if __name__ == '__main__':
    unittest.main()
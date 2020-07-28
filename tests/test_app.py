import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import App
from files_sdk import app

class AppTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        resp = app.list()

if __name__ == '__main__':
    unittest.main()
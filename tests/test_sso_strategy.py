import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SsoStrategy
from files_sdk import sso_strategy

class SsoStrategyTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        resp = sso_strategy.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sso_strategy.find(id, params)

if __name__ == '__main__':
    unittest.main()
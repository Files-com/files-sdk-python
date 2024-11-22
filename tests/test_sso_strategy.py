import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SsoStrategy
from files_sdk import sso_strategy

class SsoStrategyTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sso_strategies/{id}/sync"), "Mock path does not exist")
    def test_sync(self):
        params = {
            "id" : 12345,
        }
        sso_strategy = SsoStrategy(params)
        sso_strategy.sync(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/sso_strategies"), "Mock path does not exist")
    def test_list(self):
        resp = sso_strategy.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/sso_strategies/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sso_strategy.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sso_strategies/{id}/sync"), "Mock path does not exist")
    def test_sync(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sso_strategy.sync(id, params)

if __name__ == '__main__':
    unittest.main()
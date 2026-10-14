import unittest
from tests.base import TestBase
from files_sdk.models import SsoStrategy
from files_sdk import sso_strategy


class SsoStrategyTest(TestBase):
    # Instance Methods
    def test_instance_sync(self):
        params = {
            "id": 12345,
        }
        sso_strategy = SsoStrategy(params)
        sso_strategy.sync(params)
        self.assert_typed(sso_strategy)

    # Static Methods
    def test_list(self):
        result = sso_strategy.list()
        self.assert_returns(sso_strategy.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sso_strategy.find(id, params)
        self.assert_returns(sso_strategy.find, result)
        self.assert_typed(result)

    def test_sync(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sso_strategy.sync(id, params)
        self.assert_returns(sso_strategy.sync, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

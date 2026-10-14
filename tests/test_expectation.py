import unittest
from tests.base import TestBase
from files_sdk.models import Expectation
from files_sdk import expectation


class ExpectationTest(TestBase):
    # Instance Methods
    def test_instance_trigger_evaluation(self):
        params = {
            "id": 12345,
        }
        expectation = Expectation(params)
        result = expectation.trigger_evaluation(params)
        self.assert_returns(Expectation.trigger_evaluation, result)
        self.assert_typed(expectation)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        expectation = Expectation(params)
        result = expectation.update(params)
        self.assert_returns(Expectation.update, result)
        self.assert_typed(expectation)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        expectation = Expectation(params)
        expectation.delete(params)
        self.assert_typed(expectation)

    # Static Methods
    def test_list(self):
        result = expectation.list()
        self.assert_returns(expectation.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = expectation.find(id, params)
        self.assert_returns(expectation.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = expectation.create()
        self.assert_returns(expectation.create, result)
        self.assert_typed(result)

    def test_trigger_evaluation(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = expectation.trigger_evaluation(id, params)
        self.assert_returns(expectation.trigger_evaluation, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = expectation.update(id, params)
        self.assert_returns(expectation.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = expectation.delete(id, params)
        self.assert_returns(expectation.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

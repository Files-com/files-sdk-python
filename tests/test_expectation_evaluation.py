import unittest
from tests.base import TestBase
from files_sdk import expectation_evaluation


class ExpectationEvaluationTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = expectation_evaluation.list()
        self.assert_returns(expectation_evaluation.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = expectation_evaluation.find(id, params)
        self.assert_returns(expectation_evaluation.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

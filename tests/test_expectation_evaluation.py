import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ExpectationEvaluation
from files_sdk import expectation_evaluation

class ExpectationEvaluationTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/expectation_evaluations"), "Mock path does not exist")
    def test_list(self):
        resp = expectation_evaluation.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/expectation_evaluations/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        expectation_evaluation.find(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Expectation
from files_sdk import expectation

class ExpectationTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectations/{id}/trigger_evaluation"), "Mock path does not exist")
    def test_trigger_evaluation(self):
        params = {
            "id" : 12345,
        }
        expectation = Expectation(params)
        expectation.trigger_evaluation(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/expectations/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        expectation = Expectation(params)
        expectation.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/expectations/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        expectation = Expectation(params)
        expectation.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/expectations"), "Mock path does not exist")
    def test_list(self):
        resp = expectation.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/expectations/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        expectation.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectations"), "Mock path does not exist")
    def test_create(self):
        resp = expectation.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectations/{id}/trigger_evaluation"), "Mock path does not exist")
    def test_trigger_evaluation(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        expectation.trigger_evaluation(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/expectations/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        expectation.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/expectations/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        expectation.delete(id, params)

if __name__ == '__main__':
    unittest.main()
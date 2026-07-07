import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import KeyLifecycleRule
from files_sdk import key_lifecycle_rule

class KeyLifecycleRuleTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/key_lifecycle_rules/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        key_lifecycle_rule = KeyLifecycleRule(params)
        key_lifecycle_rule.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/key_lifecycle_rules/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        key_lifecycle_rule = KeyLifecycleRule(params)
        key_lifecycle_rule.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/key_lifecycle_rules"), "Mock path does not exist")
    def test_list(self):
        resp = key_lifecycle_rule.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/key_lifecycle_rules/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        key_lifecycle_rule.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/key_lifecycle_rules"), "Mock path does not exist")
    def test_create(self):
        resp = key_lifecycle_rule.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/key_lifecycle_rules/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        key_lifecycle_rule.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/key_lifecycle_rules/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        key_lifecycle_rule.delete(id, params)

if __name__ == '__main__':
    unittest.main()
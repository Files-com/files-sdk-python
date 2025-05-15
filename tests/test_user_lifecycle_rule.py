import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import UserLifecycleRule
from files_sdk import user_lifecycle_rule

class UserLifecycleRuleTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/user_lifecycle_rules/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        user_lifecycle_rule = UserLifecycleRule(params)
        user_lifecycle_rule.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/user_lifecycle_rules"), "Mock path does not exist")
    def test_list(self):
        resp = user_lifecycle_rule.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/user_lifecycle_rules/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user_lifecycle_rule.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/user_lifecycle_rules"), "Mock path does not exist")
    def test_create(self):
        params = {
            "action" : "foo",
            "authentication_method" : "foo",
            "inactivity_days" : 12345,
        }
        user_lifecycle_rule.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/user_lifecycle_rules/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user_lifecycle_rule.delete(id, params)

if __name__ == '__main__':
    unittest.main()
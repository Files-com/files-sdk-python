import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ChildSiteManagementPolicy
from files_sdk import child_site_management_policy

class ChildSiteManagementPolicyTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/child_site_management_policies/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        child_site_management_policy = ChildSiteManagementPolicy(params)
        child_site_management_policy.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/child_site_management_policies/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        child_site_management_policy = ChildSiteManagementPolicy(params)
        child_site_management_policy.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/child_site_management_policies"), "Mock path does not exist")
    def test_list(self):
        resp = child_site_management_policy.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/child_site_management_policies/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        child_site_management_policy.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/child_site_management_policies"), "Mock path does not exist")
    def test_create(self):
        params = {
            "policy_type" : "foo",
        }
        child_site_management_policy.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/child_site_management_policies/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        child_site_management_policy.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/child_site_management_policies/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        child_site_management_policy.delete(id, params)

if __name__ == '__main__':
    unittest.main()
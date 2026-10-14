import unittest
from tests.base import TestBase
from files_sdk.models import ChildSiteManagementPolicy
from files_sdk import child_site_management_policy


class ChildSiteManagementPolicyTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        child_site_management_policy = ChildSiteManagementPolicy(params)
        result = child_site_management_policy.update(params)
        self.assert_returns(ChildSiteManagementPolicy.update, result)
        self.assert_typed(child_site_management_policy)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        child_site_management_policy = ChildSiteManagementPolicy(params)
        child_site_management_policy.delete(params)
        self.assert_typed(child_site_management_policy)

    # Static Methods
    def test_list(self):
        result = child_site_management_policy.list()
        self.assert_returns(child_site_management_policy.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = child_site_management_policy.find(id, params)
        self.assert_returns(child_site_management_policy.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "policy_type": "foo",
        }
        result = child_site_management_policy.create(params)
        self.assert_returns(child_site_management_policy.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = child_site_management_policy.update(id, params)
        self.assert_returns(child_site_management_policy.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = child_site_management_policy.delete(id, params)
        self.assert_returns(child_site_management_policy.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

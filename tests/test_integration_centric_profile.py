import unittest
from tests.base import TestBase
from files_sdk.models import IntegrationCentricProfile
from files_sdk import integration_centric_profile


class IntegrationCentricProfileTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        integration_centric_profile = IntegrationCentricProfile(params)
        result = integration_centric_profile.update(params)
        self.assert_returns(IntegrationCentricProfile.update, result)
        self.assert_typed(integration_centric_profile)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        integration_centric_profile = IntegrationCentricProfile(params)
        integration_centric_profile.delete(params)
        self.assert_typed(integration_centric_profile)

    # Static Methods
    def test_list(self):
        result = integration_centric_profile.list()
        self.assert_returns(integration_centric_profile.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = integration_centric_profile.find(id, params)
        self.assert_returns(integration_centric_profile.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "expected_remote_servers": [{}],
        }
        result = integration_centric_profile.create(params)
        self.assert_returns(integration_centric_profile.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = integration_centric_profile.update(id, params)
        self.assert_returns(integration_centric_profile.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = integration_centric_profile.delete(id, params)
        self.assert_returns(integration_centric_profile.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

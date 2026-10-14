import unittest
from tests.base import TestBase
from files_sdk.models import DesktopConfigurationProfile
from files_sdk import desktop_configuration_profile


class DesktopConfigurationProfileTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        desktop_configuration_profile = DesktopConfigurationProfile(params)
        result = desktop_configuration_profile.update(params)
        self.assert_returns(DesktopConfigurationProfile.update, result)
        self.assert_typed(desktop_configuration_profile)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        desktop_configuration_profile = DesktopConfigurationProfile(params)
        desktop_configuration_profile.delete(params)
        self.assert_typed(desktop_configuration_profile)

    # Static Methods
    def test_list(self):
        result = desktop_configuration_profile.list()
        self.assert_returns(desktop_configuration_profile.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = desktop_configuration_profile.find(id, params)
        self.assert_returns(desktop_configuration_profile.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "mount_mappings": {},
        }
        result = desktop_configuration_profile.create(params)
        self.assert_returns(desktop_configuration_profile.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = desktop_configuration_profile.update(id, params)
        self.assert_returns(desktop_configuration_profile.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = desktop_configuration_profile.delete(id, params)
        self.assert_returns(desktop_configuration_profile.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

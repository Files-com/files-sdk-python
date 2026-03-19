import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import DesktopConfigurationProfile
from files_sdk import desktop_configuration_profile

class DesktopConfigurationProfileTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/desktop_configuration_profiles/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        desktop_configuration_profile = DesktopConfigurationProfile(params)
        desktop_configuration_profile.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/desktop_configuration_profiles/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        desktop_configuration_profile = DesktopConfigurationProfile(params)
        desktop_configuration_profile.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/desktop_configuration_profiles"), "Mock path does not exist")
    def test_list(self):
        resp = desktop_configuration_profile.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/desktop_configuration_profiles/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        desktop_configuration_profile.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/desktop_configuration_profiles"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "mount_mappings" : {},
        }
        desktop_configuration_profile.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/desktop_configuration_profiles/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        desktop_configuration_profile.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/desktop_configuration_profiles/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        desktop_configuration_profile.delete(id, params)

if __name__ == '__main__':
    unittest.main()
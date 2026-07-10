import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import IntegrationCentricProfile
from files_sdk import integration_centric_profile

class IntegrationCentricProfileTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/integration_centric_profiles/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        integration_centric_profile = IntegrationCentricProfile(params)
        integration_centric_profile.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/integration_centric_profiles/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        integration_centric_profile = IntegrationCentricProfile(params)
        integration_centric_profile.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/integration_centric_profiles"), "Mock path does not exist")
    def test_list(self):
        resp = integration_centric_profile.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/integration_centric_profiles/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        integration_centric_profile.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/integration_centric_profiles"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "expected_remote_servers" : [{}],
        }
        integration_centric_profile.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/integration_centric_profiles/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        integration_centric_profile.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/integration_centric_profiles/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        integration_centric_profile.delete(id, params)

if __name__ == '__main__':
    unittest.main()
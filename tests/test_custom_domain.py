import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import CustomDomain
from files_sdk import custom_domain

class CustomDomainTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/custom_domains/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        custom_domain = CustomDomain(params)
        custom_domain.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/custom_domains/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        custom_domain = CustomDomain(params)
        custom_domain.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/custom_domains"), "Mock path does not exist")
    def test_list(self):
        resp = custom_domain.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/custom_domains/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        custom_domain.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/custom_domains"), "Mock path does not exist")
    def test_create(self):
        params = {
            "domain" : "foo",
        }
        custom_domain.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/custom_domains/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = custom_domain.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/custom_domains/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        custom_domain.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/custom_domains/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        custom_domain.delete(id, params)

if __name__ == '__main__':
    unittest.main()
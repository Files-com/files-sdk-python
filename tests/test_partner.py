import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Partner
from files_sdk import partner

class PartnerTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/partners/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        partner = Partner(params)
        partner.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partners/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        partner = Partner(params)
        partner.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partners"), "Mock path does not exist")
    def test_list(self):
        resp = partner.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/partners/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/partners"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        partner.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/partners/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/partners/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        partner.delete(id, params)

if __name__ == '__main__':
    unittest.main()
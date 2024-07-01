import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import As2Partner
from files_sdk import as2_partner

class As2PartnerTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/as2_partners/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        as2_partner = As2Partner(params)
        as2_partner.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/as2_partners/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        as2_partner = As2Partner(params)
        as2_partner.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/as2_partners"), "Mock path does not exist")
    def test_list(self):
        resp = as2_partner.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/as2_partners/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        as2_partner.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/as2_partners"), "Mock path does not exist")
    def test_create(self):
        params = {
            "as2_station_id" : 12345,
            "name" : "foo",
            "uri" : "foo",
            "public_certificate" : "foo",
        }
        as2_partner.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/as2_partners/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        as2_partner.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/as2_partners/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        as2_partner.delete(id, params)

if __name__ == '__main__':
    unittest.main()
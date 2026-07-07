import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Certificate
from files_sdk import certificate

class CertificateTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/certificates/{id}/deactivate"), "Mock path does not exist")
    def test_deactivate(self):
        params = {
            "id" : 12345,
        }
        certificate = Certificate(params)
        certificate.deactivate(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/certificates/{id}/activate"), "Mock path does not exist")
    def test_activate(self):
        params = {
            "id" : 12345,
        }
        certificate = Certificate(params)
        certificate.activate(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/certificates/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        certificate = Certificate(params)
        certificate.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/certificates/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        certificate = Certificate(params)
        certificate.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/certificates"), "Mock path does not exist")
    def test_list(self):
        resp = certificate.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/certificates/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        certificate.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/certificates"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        certificate.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/certificates/{id}/deactivate"), "Mock path does not exist")
    def test_deactivate(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        certificate.deactivate(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/certificates/{id}/activate"), "Mock path does not exist")
    def test_activate(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        certificate.activate(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/certificates/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = certificate.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/certificates/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        certificate.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/certificates/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        certificate.delete(id, params)

if __name__ == '__main__':
    unittest.main()
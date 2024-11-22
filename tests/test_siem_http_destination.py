import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SiemHttpDestination
from files_sdk import siem_http_destination

class SiemHttpDestinationTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/siem_http_destinations/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        siem_http_destination = SiemHttpDestination(params)
        siem_http_destination.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/siem_http_destinations/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        siem_http_destination = SiemHttpDestination(params)
        siem_http_destination.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/siem_http_destinations"), "Mock path does not exist")
    def test_list(self):
        resp = siem_http_destination.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/siem_http_destinations/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        siem_http_destination.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/siem_http_destinations"), "Mock path does not exist")
    def test_create(self):
        params = {
            "destination_type" : "foo",
            "destination_url" : "foo",
        }
        siem_http_destination.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/siem_http_destinations/send_test_entry"), "Mock path does not exist")
    def test_send_test_entry(self):
        resp = siem_http_destination.send_test_entry()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/siem_http_destinations/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        siem_http_destination.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/siem_http_destinations/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        siem_http_destination.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import As2Station
from files_sdk import as2_station

class As2StationTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/as2_stations/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        as2_station = As2Station(params)
        as2_station.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/as2_stations/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        as2_station = As2Station(params)
        as2_station.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/as2_stations"), "Mock path does not exist")
    def test_list(self):
        resp = as2_station.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/as2_stations/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        as2_station.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/as2_stations"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "public_certificate" : "foo",
            "private_key" : "foo",
        }
        as2_station.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/as2_stations/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        as2_station.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/as2_stations/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        as2_station.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import RemoteServer
from files_sdk import remote_server

class RemoteServerTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/configuration_file"), "Mock path does not exist")
    def test_configuration_file(self):
        params = {
            "id" : 12345,
        }
        remote_server = RemoteServer(params)
        remote_server.configuration_file(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/remote_servers/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        remote_server = RemoteServer(params)
        remote_server.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/remote_servers/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        remote_server = RemoteServer(params)
        remote_server.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_servers"), "Mock path does not exist")
    def test_list(self):
        resp = remote_server.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_servers/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_servers/{id}/configuration_file"), "Mock path does not exist")
    def test_find_configuration_file(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.find_configuration_file(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers"), "Mock path does not exist")
    def test_create(self):
        resp = remote_server.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/configuration_file"), "Mock path does not exist")
    def test_configuration_file(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.configuration_file(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/remote_servers/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/remote_servers/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.delete(id, params)

if __name__ == '__main__':
    unittest.main()
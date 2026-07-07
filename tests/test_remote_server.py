import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import RemoteServer
from files_sdk import remote_server

class RemoteServerTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/agent_push_update"), "Mock path does not exist")
    def test_agent_push_update(self):
        params = {
            "id" : 12345,
        }
        remote_server = RemoteServer(params)
        remote_server.agent_push_update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/disconnect_agent"), "Mock path does not exist")
    def test_disconnect_agent(self):
        params = {
            "id" : 12345,
        }
        remote_server = RemoteServer(params)
        remote_server.disconnect_agent(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/authenticate_agent"), "Mock path does not exist")
    def test_authenticate_agent(self):
        params = {
            "id" : 12345,
        }
        remote_server = RemoteServer(params)
        remote_server.authenticate_agent(params)

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

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/remote_servers/{id}/ping_agent"), "Mock path does not exist")
    def test_find_ping_agent(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.find_ping_agent(id, params)

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

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/agent_push_update"), "Mock path does not exist")
    def test_agent_push_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.agent_push_update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/disconnect_agent"), "Mock path does not exist")
    def test_disconnect_agent(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.disconnect_agent(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/authenticate_agent"), "Mock path does not exist")
    def test_authenticate_agent(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.authenticate_agent(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/{id}/configuration_file"), "Mock path does not exist")
    def test_configuration_file(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.configuration_file(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/remote_servers/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = remote_server.create_export()


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
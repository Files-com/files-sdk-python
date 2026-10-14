import unittest
from tests.base import TestBase
from files_sdk.models import RemoteServer
from files_sdk import remote_server


class RemoteServerTest(TestBase):
    # Instance Methods
    def test_instance_agent_nodes(self):
        params = {
            "id": 12345,
        }
        remote_server = RemoteServer(params)
        result = remote_server.agent_nodes(params)
        self.assert_returns(RemoteServer.agent_nodes, result)
        self.assert_typed(remote_server)

    def test_instance_agent_push_update(self):
        params = {
            "id": 12345,
        }
        remote_server = RemoteServer(params)
        result = remote_server.agent_push_update(params)
        self.assert_returns(RemoteServer.agent_push_update, result)
        self.assert_typed(remote_server)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        remote_server = RemoteServer(params)
        result = remote_server.update(params)
        self.assert_returns(RemoteServer.update, result)
        self.assert_typed(remote_server)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        remote_server = RemoteServer(params)
        remote_server.delete(params)
        self.assert_typed(remote_server)

    # Static Methods
    def test_list(self):
        result = remote_server.list()
        self.assert_returns(remote_server.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server.find(id, params)
        self.assert_returns(remote_server.find, result)
        self.assert_typed(result)

    def test_agent_nodes(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server.agent_nodes(id, params)
        self.assert_returns(remote_server.agent_nodes, result)
        self.assert_typed(result)

    def test_find_configuration_file(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server.find_configuration_file(id, params)
        self.assert_returns(remote_server.find_configuration_file, result)
        self.assert_typed(result)

    def test_create(self):
        result = remote_server.create()
        self.assert_returns(remote_server.create, result)
        self.assert_typed(result)

    def test_agent_push_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server.agent_push_update(id, params)
        self.assert_returns(remote_server.agent_push_update, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server.update(id, params)
        self.assert_returns(remote_server.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = remote_server.delete(id, params)
        self.assert_returns(remote_server.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

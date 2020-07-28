import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import RemoteServer
from files_sdk import remote_server

class RemoteServerTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
        }
        remote_server = RemoteServer(params)
        remote_server.update(params)

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
    def test_list(self):
        resp = remote_server.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.find(id, params)

    def test_create(self):
        resp = remote_server.create()

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        remote_server.delete(id, params)

if __name__ == '__main__':
    unittest.main()
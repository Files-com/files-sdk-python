import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Workspace
from files_sdk import workspace

class WorkspaceTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/workspaces/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        workspace = Workspace(params)
        workspace.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/workspaces/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        workspace = Workspace(params)
        workspace.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/workspaces"), "Mock path does not exist")
    def test_list(self):
        resp = workspace.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/workspaces/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        workspace.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/workspaces"), "Mock path does not exist")
    def test_create(self):
        resp = workspace.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/workspaces/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        workspace.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/workspaces/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        workspace.delete(id, params)

if __name__ == '__main__':
    unittest.main()
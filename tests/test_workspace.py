import unittest
from tests.base import TestBase
from files_sdk.models import Workspace
from files_sdk import workspace


class WorkspaceTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        workspace = Workspace(params)
        result = workspace.update(params)
        self.assert_returns(Workspace.update, result)
        self.assert_typed(workspace)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        workspace = Workspace(params)
        workspace.delete(params)
        self.assert_typed(workspace)

    # Static Methods
    def test_list(self):
        result = workspace.list()
        self.assert_returns(workspace.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = workspace.find(id, params)
        self.assert_returns(workspace.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = workspace.create()
        self.assert_returns(workspace.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = workspace.update(id, params)
        self.assert_returns(workspace.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = workspace.delete(id, params)
        self.assert_returns(workspace.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

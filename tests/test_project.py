import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Project
from files_sdk import project

class ProjectTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/projects/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
            "global_access" : "foo",
        }
        project = Project(params)
        project.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/projects/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        project = Project(params)
        project.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/projects"), "Mock path does not exist")
    def test_list(self):
        resp = project.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/projects/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        project.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/projects"), "Mock path does not exist")
    def test_create(self):
        params = {
            "global_access" : "foo",
        }
        project.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/projects/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "global_access" : "foo",
        }
        project.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/projects/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        project.delete(id, params)

if __name__ == '__main__':
    unittest.main()
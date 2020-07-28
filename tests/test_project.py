import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Project
from files_sdk import project

class ProjectTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "global_access" : "foo",
        }
        project = Project(params)
        project.update(params)

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
    def test_list(self):
        resp = project.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        project.find(id, params)

    def test_create(self):
        params = {
            "global_access" : "foo",
        }
        project.create(params)

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "global_access" : "foo",
        }
        project.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        project.delete(id, params)

if __name__ == '__main__':
    unittest.main()
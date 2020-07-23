import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Project

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
    def test_do_list(self):
        resp = Project.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Project.do_find(id, params)

    def test_do_create(self):
        params = {
            "global_access" : "foo",
        }
        Project.do_create(params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "global_access" : "foo",
        }
        Project.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Project.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
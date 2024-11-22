import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ShareGroup
from files_sdk import share_group

class ShareGroupTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/share_groups/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        share_group = ShareGroup(params)
        share_group.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/share_groups/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        share_group = ShareGroup(params)
        share_group.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/share_groups"), "Mock path does not exist")
    def test_list(self):
        resp = share_group.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/share_groups/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        share_group.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/share_groups"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "members" : [{}],
        }
        share_group.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/share_groups/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        share_group.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/share_groups/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        share_group.delete(id, params)

if __name__ == '__main__':
    unittest.main()
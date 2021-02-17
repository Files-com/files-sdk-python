import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FileComment
from files_sdk import file_comment

class FileCommentTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/file_comments/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
            "body" : "foo",
        }
        file_comment = FileComment(params)
        file_comment.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/file_comments/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        file_comment = FileComment(params)
        file_comment.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/file_comments/files/{path}"), "Mock path does not exist")
    def test_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file_comment.list_for(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/file_comments"), "Mock path does not exist")
    def test_create(self):
        params = {
            "body" : "foo",
            "path" : "foo",
        }
        file_comment.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/file_comments/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "body" : "foo",
        }
        file_comment.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/file_comments/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        file_comment.delete(id, params)

if __name__ == '__main__':
    unittest.main()
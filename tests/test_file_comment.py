import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import FileComment

class FileCommentTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "body" : "foo",
        }
        file_comment = FileComment(params)
        file_comment.update(params)

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
    def test_do_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        FileComment.do_list_for(path, params)

    def test_do_create(self):
        params = {
            "body" : "foo",
            "path" : "foo",
        }
        FileComment.do_create(params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "body" : "foo",
        }
        FileComment.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        FileComment.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
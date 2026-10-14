import unittest
from tests.base import TestBase
from files_sdk.models import FileComment
from files_sdk import file_comment


class FileCommentTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
            "body": "foo",
        }
        file_comment = FileComment(params)
        result = file_comment.update(params)
        self.assert_returns(FileComment.update, result)
        self.assert_typed(file_comment)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        file_comment = FileComment(params)
        file_comment.delete(params)
        self.assert_typed(file_comment)

    # Static Methods
    def test_list_for(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file_comment.list_for(path, params)
        self.assert_returns(file_comment.list_for, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "body": "foo",
            "path": "foo",
        }
        result = file_comment.create(params)
        self.assert_returns(file_comment.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
            "body": "foo",
        }
        result = file_comment.update(id, params)
        self.assert_returns(file_comment.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = file_comment.delete(id, params)
        self.assert_returns(file_comment.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

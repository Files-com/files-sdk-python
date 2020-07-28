import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import MessageComment
from files_sdk import message_comment

class MessageCommentTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "body" : "foo",
        }
        message_comment = MessageComment(params)
        message_comment.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        message_comment = MessageComment(params)
        message_comment.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        params = {
            "message_id" : 12345,
        }
        message_comment.list(params)

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        message_comment.find(id, params)

    def test_create(self):
        params = {
            "body" : "foo",
        }
        message_comment.create(params)

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "body" : "foo",
        }
        message_comment.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        message_comment.delete(id, params)

if __name__ == '__main__':
    unittest.main()
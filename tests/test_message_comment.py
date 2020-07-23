import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import MessageComment

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
    def test_do_list(self):
        params = {
            "message_id" : 12345,
        }
        MessageComment.do_list(params)

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        MessageComment.do_find(id, params)

    def test_do_create(self):
        params = {
            "body" : "foo",
        }
        MessageComment.do_create(params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "body" : "foo",
        }
        MessageComment.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        MessageComment.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
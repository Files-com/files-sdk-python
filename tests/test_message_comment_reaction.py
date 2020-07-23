import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import MessageCommentReaction

class MessageCommentReactionTest(TestBase):
    pass 
    # Instance Methods
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        message_comment_reaction = MessageCommentReaction(params)
        message_comment_reaction.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_list(self):
        params = {
            "message_comment_id" : 12345,
        }
        MessageCommentReaction.do_list(params)

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        MessageCommentReaction.do_find(id, params)

    def test_do_create(self):
        params = {
            "emoji" : "foo",
        }
        MessageCommentReaction.do_create(params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        MessageCommentReaction.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
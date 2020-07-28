import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import MessageCommentReaction
from files_sdk import message_comment_reaction

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
    def test_list(self):
        params = {
            "message_comment_id" : 12345,
        }
        message_comment_reaction.list(params)

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        message_comment_reaction.find(id, params)

    def test_create(self):
        params = {
            "emoji" : "foo",
        }
        message_comment_reaction.create(params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        message_comment_reaction.delete(id, params)

if __name__ == '__main__':
    unittest.main()
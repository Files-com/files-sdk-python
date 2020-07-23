import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import MessageReaction

class MessageReactionTest(TestBase):
    pass 
    # Instance Methods
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        message_reaction = MessageReaction(params)
        message_reaction.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_list(self):
        params = {
            "message_id" : 12345,
        }
        MessageReaction.do_list(params)

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        MessageReaction.do_find(id, params)

    def test_do_create(self):
        params = {
            "emoji" : "foo",
        }
        MessageReaction.do_create(params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        MessageReaction.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
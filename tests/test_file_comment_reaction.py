import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import FileCommentReaction

class FileCommentReactionTest(TestBase):
    pass 
    # Instance Methods
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        file_comment_reaction = FileCommentReaction(params)
        file_comment_reaction.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_create(self):
        params = {
            "file_comment_id" : 12345,
            "emoji" : "foo",
        }
        FileCommentReaction.do_create(params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        FileCommentReaction.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
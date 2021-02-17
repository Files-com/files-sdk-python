import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FileCommentReaction
from files_sdk import file_comment_reaction

class FileCommentReactionTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/file_comment_reactions/{id}"), "Mock path does not exist")
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
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/file_comment_reactions"), "Mock path does not exist")
    def test_create(self):
        params = {
            "file_comment_id" : 12345,
            "emoji" : "foo",
        }
        file_comment_reaction.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/file_comment_reactions/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        file_comment_reaction.delete(id, params)

if __name__ == '__main__':
    unittest.main()
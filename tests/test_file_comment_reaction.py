import unittest
from tests.base import TestBase
from files_sdk.models import FileCommentReaction
from files_sdk import file_comment_reaction


class FileCommentReactionTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        file_comment_reaction = FileCommentReaction(params)
        file_comment_reaction.delete(params)
        self.assert_typed(file_comment_reaction)

    # Static Methods
    def test_create(self):
        params = {
            "file_comment_id": 12345,
            "emoji": "foo",
        }
        result = file_comment_reaction.create(params)
        self.assert_returns(file_comment_reaction.create, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = file_comment_reaction.delete(id, params)
        self.assert_returns(file_comment_reaction.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

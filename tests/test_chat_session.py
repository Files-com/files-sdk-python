import unittest
from tests.base import TestBase
from files_sdk import chat_session


class ChatSessionTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = chat_session.list()
        self.assert_returns(chat_session.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = "foo"
        params = {
            "id": "foo",
        }
        result = chat_session.find(id, params)
        self.assert_returns(chat_session.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

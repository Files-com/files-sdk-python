import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ChatSession
from files_sdk import chat_session

class ChatSessionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/chat_sessions"), "Mock path does not exist")
    def test_list(self):
        resp = chat_session.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/chat_sessions/{id}"), "Mock path does not exist")
    def test_find(self):
        id = "foo"
        params = {
            "id" : "foo",
        }
        chat_session.find(id, params)

if __name__ == '__main__':
    unittest.main()
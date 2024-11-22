import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import EmailIncomingMessage
from files_sdk import email_incoming_message

class EmailIncomingMessageTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/email_incoming_messages"), "Mock path does not exist")
    def test_list(self):
        resp = email_incoming_message.list()

if __name__ == '__main__':
    unittest.main()
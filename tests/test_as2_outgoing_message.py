import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import As2OutgoingMessage
from files_sdk import as2_outgoing_message

class As2OutgoingMessageTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/as2_outgoing_messages"), "Mock path does not exist")
    def test_list(self):
        resp = as2_outgoing_message.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/as2_outgoing_messages/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = as2_outgoing_message.create_export()

if __name__ == '__main__':
    unittest.main()
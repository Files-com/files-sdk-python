import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import As2IncomingMessage
from files_sdk import as2_incoming_message

class As2IncomingMessageTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/as2_incoming_messages"), "Mock path does not exist")
    def test_list(self):
        resp = as2_incoming_message.list()

if __name__ == '__main__':
    unittest.main()
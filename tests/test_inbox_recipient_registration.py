import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import InboxRecipientRegistration
from files_sdk import inbox_recipient_registration

class InboxRecipientRegistrationTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/inbox_recipient_registrations"), "Mock path does not exist")
    def test_create(self):
        params = {
            "inbox_recipient_code" : "foo",
        }
        inbox_recipient_registration.create(params)

if __name__ == '__main__':
    unittest.main()
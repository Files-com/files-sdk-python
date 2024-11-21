import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import InboxRegistration
from files_sdk import inbox_registration

class InboxRegistrationTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/inbox_registrations"), "Mock path does not exist")
    def test_list(self):
        resp = inbox_registration.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/inbox_registrations/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = inbox_registration.create_export()

if __name__ == '__main__':
    unittest.main()
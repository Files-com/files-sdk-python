import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import BundleRecipientRegistration
from files_sdk import bundle_recipient_registration

class BundleRecipientRegistrationTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/bundle_recipient_registrations"), "Mock path does not exist")
    def test_create(self):
        params = {
            "bundle_recipient_code" : "foo",
        }
        bundle_recipient_registration.create(params)

if __name__ == '__main__':
    unittest.main()
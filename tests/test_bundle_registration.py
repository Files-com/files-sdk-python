import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import BundleRegistration
from files_sdk import bundle_registration

class BundleRegistrationTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bundle_registrations"), "Mock path does not exist")
    def test_list(self):
        resp = bundle_registration.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/bundle_registrations/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = bundle_registration.create_export()

if __name__ == '__main__':
    unittest.main()
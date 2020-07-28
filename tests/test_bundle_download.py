import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import BundleDownload
from files_sdk import bundle_download

class BundleDownloadTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        params = {
            "bundle_registration_id" : 12345,
        }
        bundle_download.list(params)

if __name__ == '__main__':
    unittest.main()
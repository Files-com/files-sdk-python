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
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bundle_downloads"), "Mock path does not exist")
    def test_list(self):
        resp = bundle_download.list()

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import BundleDownload

class BundleDownloadTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        params = {
            "bundle_registration_id" : 12345,
        }
        BundleDownload.do_list(params)

if __name__ == '__main__':
    unittest.main()
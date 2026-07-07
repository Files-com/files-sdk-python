import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ZipDownload
from files_sdk import zip_download

class ZipDownloadTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/zip_downloads"), "Mock path does not exist")
    def test_create(self):
        params = {
            "paths" : ["foo1"],
        }
        zip_download.create(params)

if __name__ == '__main__':
    unittest.main()
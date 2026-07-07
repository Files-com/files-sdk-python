import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ZipDownloadFile
from files_sdk import zip_download_file

class ZipDownloadFileTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/zip_download_files"), "Mock path does not exist")
    def test_create(self):
        params = {
            "code" : "foo",
        }
        zip_download_file.create(params)

if __name__ == '__main__':
    unittest.main()
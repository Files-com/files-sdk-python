import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import PublicUrl
from files_sdk import public_url

class PublicUrlTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/public_urls"), "Mock path does not exist")
    def test_create(self):
        path = "foo"
        params = {
            "hostname" : "foo",
            "path" : "foo",
        }
        public_url.create(path, params)

if __name__ == '__main__':
    unittest.main()
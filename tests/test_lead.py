import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Lead
from files_sdk import lead

class LeadTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/leads"), "Mock path does not exist")
    def test_create(self):
        resp = lead.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/leads/{code}"), "Mock path does not exist")
    def test_update(self):
        code = "foo"
        params = {
            "code" : "foo",
        }
        lead.update(code, params)

if __name__ == '__main__':
    unittest.main()
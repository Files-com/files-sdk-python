import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ClickwrapAcceptance
from files_sdk import clickwrap_acceptance

class ClickwrapAcceptanceTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/clickwrap_acceptances"), "Mock path does not exist")
    def test_create(self):
        params = {
            "clickwrap_id" : 12345,
        }
        clickwrap_acceptance.create(params)

if __name__ == '__main__':
    unittest.main()
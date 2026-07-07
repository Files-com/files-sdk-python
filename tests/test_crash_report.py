import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import CrashReport
from files_sdk import crash_report

class CrashReportTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/crash_reports"), "Mock path does not exist")
    def test_create(self):
        params = {
            "build" : "foo",
            "platform" : "foo",
            "product_name" : "foo",
            "version" : "foo",
        }
        crash_report.create(params)

if __name__ == '__main__':
    unittest.main()
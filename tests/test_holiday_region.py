import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import HolidayRegion
from files_sdk import holiday_region

class HolidayRegionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/holiday_regions/supported"), "Mock path does not exist")
    def test_get_supported(self):
        resp = holiday_region.get_supported()

if __name__ == '__main__':
    unittest.main()
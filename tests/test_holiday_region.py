import unittest
from tests.base import TestBase
from files_sdk import holiday_region


class HolidayRegionTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_get_supported(self):
        result = holiday_region.get_supported()
        self.assert_returns(holiday_region.get_supported, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

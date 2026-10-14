import unittest
from tests.base import TestBase
from files_sdk import site


class SiteTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_get(self):
        result = site.get()
        self.assert_returns(site.get, result)
        self.assert_typed(result)

    def test_get_usage(self):
        result = site.get_usage()
        self.assert_returns(site.get_usage, result)
        self.assert_typed(result)

    def test_update(self):
        result = site.update()
        self.assert_returns(site.update, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

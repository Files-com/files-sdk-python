import unittest
from tests.base import TestBase
from files_sdk import bundle_registration


class BundleRegistrationTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = bundle_registration.list()
        self.assert_returns(bundle_registration.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

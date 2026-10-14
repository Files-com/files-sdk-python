import unittest
from tests.base import TestBase
from files_sdk import bundle_download


class BundleDownloadTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = bundle_download.list()
        self.assert_returns(bundle_download.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

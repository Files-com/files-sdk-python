import unittest
from tests.base import TestBase
from files_sdk import bundle_recipient


class BundleRecipientTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        params = {
            "bundle_id": 12345,
        }
        result = bundle_recipient.list(params)
        self.assert_returns(bundle_recipient.list, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "bundle_id": 12345,
            "recipient": "foo",
        }
        result = bundle_recipient.create(params)
        self.assert_returns(bundle_recipient.create, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

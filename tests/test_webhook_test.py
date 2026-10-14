import unittest
from tests.base import TestBase
from files_sdk import webhook_test


class WebhookTestTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_create(self):
        params = {
            "url": "foo",
        }
        result = webhook_test.create(params)
        self.assert_returns(webhook_test.create, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

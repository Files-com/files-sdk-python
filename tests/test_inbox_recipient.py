import unittest
from tests.base import TestBase
from files_sdk import inbox_recipient


class InboxRecipientTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        params = {
            "inbox_id": 12345,
        }
        result = inbox_recipient.list(params)
        self.assert_returns(inbox_recipient.list, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "inbox_id": 12345,
            "recipient": "foo",
        }
        result = inbox_recipient.create(params)
        self.assert_returns(inbox_recipient.create, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

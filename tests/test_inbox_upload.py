import unittest
from tests.base import TestBase
from files_sdk import inbox_upload


class InboxUploadTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = inbox_upload.list()
        self.assert_returns(inbox_upload.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

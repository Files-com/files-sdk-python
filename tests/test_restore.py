import unittest
from tests.base import TestBase
from files_sdk import restore


class RestoreTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = restore.list()
        self.assert_returns(restore.list, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "earliest_date": "foo",
        }
        result = restore.create(params)
        self.assert_returns(restore.create, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk import app


class AppTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = app.list()
        self.assert_returns(app.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

import unittest
from tests.base import TestBase
from files_sdk import session


class SessionTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_create(self):
        result = session.create()
        self.assert_returns(session.create, result)
        self.assert_typed(result)

    def test_delete(self):
        result = session.delete()
        self.assert_returns(session.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

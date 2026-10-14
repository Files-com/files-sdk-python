import unittest
from tests.base import TestBase
from files_sdk import user_security_event


class UserSecurityEventTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = user_security_event.list()
        self.assert_returns(user_security_event.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_security_event.find(id, params)
        self.assert_returns(user_security_event.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

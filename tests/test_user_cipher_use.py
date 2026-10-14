import unittest
from tests.base import TestBase
from files_sdk import user_cipher_use


class UserCipherUseTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = user_cipher_use.list()
        self.assert_returns(user_cipher_use.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

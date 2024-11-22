import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import UserCipherUse
from files_sdk import user_cipher_use

class UserCipherUseTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/user_cipher_uses"), "Mock path does not exist")
    def test_list(self):
        resp = user_cipher_use.list()

if __name__ == '__main__':
    unittest.main()
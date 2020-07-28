import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import User
from files_sdk import user

class UserTest(TestBase):
    pass 
    # Instance Methods
    def test_unlock(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.unlock(params)

    def test_resend_welcome_email(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.resend_welcome_email(params)

    def test_user_2fa_reset(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.user_2fa_reset(params)

    def test_update(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = user.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.find(id, params)

    def test_create(self):
        resp = user.create()

    def test_unlock(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.unlock(id, params)

    def test_resend_welcome_email(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.resend_welcome_email(id, params)

    def test_user_2fa_reset(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.user_2fa_reset(id, params)

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.delete(id, params)

if __name__ == '__main__':
    unittest.main()
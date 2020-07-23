import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import User

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
    def test_do_list(self):
        resp = User.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        User.do_find(id, params)

    def test_do_create(self):
        resp = User.do_create()

    def test_do_unlock(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        User.do_unlock(id, params)

    def test_do_resend_welcome_email(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        User.do_resend_welcome_email(id, params)

    def test_do_user_2fa_reset(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        User.do_user_2fa_reset(id, params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        User.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        User.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
from tests.base import TestBase
from files_sdk.models import User
from files_sdk import user


class UserTest(TestBase):
    # Instance Methods
    def test_instance_unlock(self):
        params = {
            "id": 12345,
        }
        user = User(params)
        user.unlock(params)
        self.assert_typed(user)

    def test_instance_resend_welcome_email(self):
        params = {
            "id": 12345,
        }
        user = User(params)
        user.resend_welcome_email(params)
        self.assert_typed(user)

    def test_instance_user_2fa_reset(self):
        params = {
            "id": 12345,
        }
        user = User(params)
        user.user_2fa_reset(params)
        self.assert_typed(user)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        user = User(params)
        result = user.update(params)
        self.assert_returns(User.update, result)
        self.assert_typed(user)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        user = User(params)
        user.delete(params)
        self.assert_typed(user)

    # Static Methods
    def test_list(self):
        result = user.list()
        self.assert_returns(user.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user.find(id, params)
        self.assert_returns(user.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "username": "foo",
        }
        result = user.create(params)
        self.assert_returns(user.create, result)
        self.assert_typed(result)

    def test_unlock(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user.unlock(id, params)
        self.assert_returns(user.unlock, result)
        self.assert_typed(result)

    def test_resend_welcome_email(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user.resend_welcome_email(id, params)
        self.assert_returns(user.resend_welcome_email, result)
        self.assert_typed(result)

    def test_user_2fa_reset(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user.user_2fa_reset(id, params)
        self.assert_returns(user.user_2fa_reset, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user.update(id, params)
        self.assert_returns(user.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user.delete(id, params)
        self.assert_returns(user.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

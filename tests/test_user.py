import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import User
from files_sdk import user

class UserTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/users/{id}/unlock"), "Mock path does not exist")
    def test_unlock(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.unlock(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/users/{id}/resend_welcome_email"), "Mock path does not exist")
    def test_resend_welcome_email(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.resend_welcome_email(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/users/{id}/2fa/reset"), "Mock path does not exist")
    def test_user_2fa_reset(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.user_2fa_reset(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/users/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        user = User(params)
        user.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/users/{id}"), "Mock path does not exist")
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
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/users"), "Mock path does not exist")
    def test_list(self):
        resp = user.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/users/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/users"), "Mock path does not exist")
    def test_create(self):
        params = {
            "username" : "foo",
        }
        user.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/users/{id}/unlock"), "Mock path does not exist")
    def test_unlock(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.unlock(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/users/{id}/resend_welcome_email"), "Mock path does not exist")
    def test_resend_welcome_email(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.resend_welcome_email(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/users/{id}/2fa/reset"), "Mock path does not exist")
    def test_user_2fa_reset(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.user_2fa_reset(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/users/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/users/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user.delete(id, params)

if __name__ == '__main__':
    unittest.main()
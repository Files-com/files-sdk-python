import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Session
from files_sdk import session

class SessionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions"), "Mock path does not exist")
    def test_create(self):
        resp = session.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/subdomain"), "Mock path does not exist")
    def test_subdomain(self):
        params = {
            "subdomain" : "foo",
        }
        session.subdomain(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/as_user"), "Mock path does not exist")
    def test_as_user(self):
        params = {
            "user_id" : "foo",
        }
        session.as_user(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/trusted"), "Mock path does not exist")
    def test_trusted(self):
        params = {
            "session_id" : "foo",
        }
        session.trusted(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/forgot/reset"), "Mock path does not exist")
    def test_forgot_reset(self):
        params = {
            "code" : "foo",
            "password" : "foo",
        }
        session.forgot_reset(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/forgot/validate"), "Mock path does not exist")
    def test_forgot_validate(self):
        params = {
            "code" : "foo",
        }
        session.forgot_validate(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/forgot"), "Mock path does not exist")
    def test_forgot(self):
        resp = session.forgot()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/public_hosting"), "Mock path does not exist")
    def test_public_hosting(self):
        params = {
            "return_to" : "foo",
        }
        session.public_hosting(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/pairing_key/{key}"), "Mock path does not exist")
    def test_pairing_key(self):
        key = "foo"
        params = {
            "key" : "foo",
        }
        session.pairing_key(key, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/sessions/oauth"), "Mock path does not exist")
    def test_oauth(self):
        params = {
            "provider" : "foo",
        }
        session.oauth(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/sessions"), "Mock path does not exist")
    def test_delete(self):
        resp = session.delete()

if __name__ == '__main__':
    unittest.main()
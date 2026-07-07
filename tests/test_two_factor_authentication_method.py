import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import TwoFactorAuthenticationMethod
from files_sdk import two_factor_authentication_method

class TwoFactorAuthenticationMethodTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/2fa/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        two_factor_authentication_method = TwoFactorAuthenticationMethod(params)
        two_factor_authentication_method.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/2fa/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        two_factor_authentication_method = TwoFactorAuthenticationMethod(params)
        two_factor_authentication_method.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/2fa"), "Mock path does not exist")
    def test_get(self):
        resp = two_factor_authentication_method.get()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/2fa"), "Mock path does not exist")
    def test_create(self):
        params = {
            "method_type" : "foo",
        }
        two_factor_authentication_method.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/2fa/send_code"), "Mock path does not exist")
    def test_send_code(self):
        resp = two_factor_authentication_method.send_code()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/2fa/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = two_factor_authentication_method.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/2fa/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        two_factor_authentication_method.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/2fa/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        two_factor_authentication_method.delete(id, params)

if __name__ == '__main__':
    unittest.main()
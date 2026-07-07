import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Site
from files_sdk import site

class SiteTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/site/plan"), "Mock path does not exist")
    def test_update_plan(self):
        params = {
            "id" : 12345,
        }
        site = Site(params)
        site.update_plan(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site"), "Mock path does not exist")
    def test_get(self):
        resp = site.get()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site/usage"), "Mock path does not exist")
    def test_get_usage(self):
        resp = site.get_usage()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site/switch_to_plan"), "Mock path does not exist")
    def test_get_switch_to_plan(self):
        resp = site.get_switch_to_plan()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site/plan"), "Mock path does not exist")
    def test_get_plan(self):
        resp = site.get_plan()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site/paypal_express_info"), "Mock path does not exist")
    def test_get_paypal_express_info(self):
        params = {
            "paypal_token" : "foo",
        }
        site.get_paypal_express_info(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/site/paypal_express"), "Mock path does not exist")
    def test_get_paypal_express(self):
        params = {
            "return_to_url" : "foo",
        }
        site.get_paypal_express(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/site/mover_trial_code"), "Mock path does not exist")
    def test_mover_trial_code(self):
        params = {
            "code" : "foo",
        }
        site.mover_trial_code(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/site"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "email" : "foo",
            "lead_cookie_code" : "foo",
            "recaptcha_token" : "foo",
        }
        site.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/site"), "Mock path does not exist")
    def test_update(self):
        resp = site.update()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/site/plan"), "Mock path does not exist")
    def test_update_plan(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        site.update_plan(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/site"), "Mock path does not exist")
    def test_delete(self):
        resp = site.delete()

if __name__ == '__main__':
    unittest.main()
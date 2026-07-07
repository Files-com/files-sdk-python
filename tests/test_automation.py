import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Automation
from files_sdk import automation

class AutomationTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/automations/{id}/manual_run"), "Mock path does not exist")
    def test_manual_run(self):
        params = {
            "id" : 12345,
        }
        automation = Automation(params)
        automation.manual_run(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/automations/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        automation = Automation(params)
        automation.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/automations/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        automation = Automation(params)
        automation.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/automations"), "Mock path does not exist")
    def test_list(self):
        resp = automation.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/automations/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/automations"), "Mock path does not exist")
    def test_create(self):
        params = {
            "automation" : "foo",
        }
        automation.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/automations/{id}/manual_run"), "Mock path does not exist")
    def test_manual_run(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation.manual_run(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/automations/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/automations/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation.delete(id, params)

if __name__ == '__main__':
    unittest.main()
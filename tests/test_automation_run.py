import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import AutomationRun
from files_sdk import automation_run

class AutomationRunTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/automation_runs/{id}/cancel"), "Mock path does not exist")
    def test_cancel(self):
        params = {
            "id" : 12345,
        }
        automation_run = AutomationRun(params)
        automation_run.cancel(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/automation_runs/{id}/rerun"), "Mock path does not exist")
    def test_rerun(self):
        params = {
            "id" : 12345,
            "node_id" : "foo",
        }
        automation_run = AutomationRun(params)
        automation_run.rerun(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/automation_runs"), "Mock path does not exist")
    def test_list(self):
        params = {
            "automation_id" : 12345,
        }
        automation_run.list(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/automation_runs/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation_run.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/automation_runs/{id}/node"), "Mock path does not exist")
    def test_find_node(self):
        id = 12345
        params = {
            "id" : 12345,
            "node_id" : "foo",
        }
        automation_run.find_node(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/automation_runs/{id}/cancel"), "Mock path does not exist")
    def test_cancel(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation_run.cancel(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/automation_runs/{id}/rerun"), "Mock path does not exist")
    def test_rerun(self):
        id = 12345
        params = {
            "id" : 12345,
            "node_id" : "foo",
        }
        automation_run.rerun(id, params)

if __name__ == '__main__':
    unittest.main()
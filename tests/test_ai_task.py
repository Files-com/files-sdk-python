import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import AiTask
from files_sdk import ai_task

class AiTaskTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ai_tasks/{id}/manual_run"), "Mock path does not exist")
    def test_manual_run(self):
        params = {
            "id" : 12345,
        }
        ai_task = AiTask(params)
        ai_task.manual_run(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/ai_tasks/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        ai_task = AiTask(params)
        ai_task.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/ai_tasks/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        ai_task = AiTask(params)
        ai_task.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ai_tasks"), "Mock path does not exist")
    def test_list(self):
        resp = ai_task.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ai_tasks/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ai_task.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ai_tasks"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "prompt" : "foo",
        }
        ai_task.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ai_tasks/{id}/manual_run"), "Mock path does not exist")
    def test_manual_run(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ai_task.manual_run(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ai_tasks/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = ai_task.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/ai_tasks/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ai_task.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/ai_tasks/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        ai_task.delete(id, params)

if __name__ == '__main__':
    unittest.main()
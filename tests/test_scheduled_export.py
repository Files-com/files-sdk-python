import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ScheduledExport
from files_sdk import scheduled_export

class ScheduledExportTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/scheduled_exports/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        scheduled_export = ScheduledExport(params)
        scheduled_export.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/scheduled_exports/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        scheduled_export = ScheduledExport(params)
        scheduled_export.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/scheduled_exports"), "Mock path does not exist")
    def test_list(self):
        resp = scheduled_export.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/scheduled_exports/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        scheduled_export.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/scheduled_exports"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "export_type" : "foo",
        }
        scheduled_export.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/scheduled_exports/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = scheduled_export.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/scheduled_exports/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        scheduled_export.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/scheduled_exports/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        scheduled_export.delete(id, params)

if __name__ == '__main__':
    unittest.main()
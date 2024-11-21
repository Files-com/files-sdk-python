import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import History
from files_sdk import history

class HistoryTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/history/files/{path}"), "Mock path does not exist")
    def test_list_for_file(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        history.list_for_file(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/history/folders/{path}"), "Mock path does not exist")
    def test_list_for_folder(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        history.list_for_folder(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/history/users/{user_id}"), "Mock path does not exist")
    def test_list_for_user(self):
        user_id = 12345
        params = {
            "user_id" : 12345,
        }
        history.list_for_user(user_id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/history/login"), "Mock path does not exist")
    def test_list_logins(self):
        resp = history.list_logins()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/history"), "Mock path does not exist")
    def test_list(self):
        resp = history.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/history/files/{path}/create_export"), "Mock path does not exist")
    def test_list_for_file_create_export(self):
        path = 12345
        params = {
            "path" : 12345,
        }
        history.list_for_file_create_export(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/history/folders/{path}/create_export"), "Mock path does not exist")
    def test_list_for_folder_create_export(self):
        path = 12345
        params = {
            "path" : 12345,
        }
        history.list_for_folder_create_export(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/history/users/{user_id}/create_export"), "Mock path does not exist")
    def test_list_for_user_create_export(self):
        user_id = 12345
        params = {
            "user_id" : 12345,
        }
        history.list_for_user_create_export(user_id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/history/login/create_export"), "Mock path does not exist")
    def test_list_logins_create_export(self):
        resp = history.list_logins_create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/history/create_export"), "Mock path does not exist")
    def test_list_create_export(self):
        resp = history.list_create_export()

if __name__ == '__main__':
    unittest.main()
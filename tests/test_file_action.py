import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FileAction
from files_sdk import file_action

class FileActionTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/file_actions/copy/{path}"), "Mock path does not exist")
    def test_copy(self):
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        file_action = FileAction(params)
        file_action.copy(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/file_actions/move/{path}"), "Mock path does not exist")
    def test_move(self):
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        file_action = FileAction(params)
        file_action.move(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/file_actions/begin_upload/{path}"), "Mock path does not exist")
    def test_begin_upload(self):
        params = {
            "path" : "foo",
        }
        file_action = FileAction(params)
        file_action.begin_upload(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/file_actions/copy/{path}"), "Mock path does not exist")
    def test_copy(self):
        path = "foo"
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        file_action.copy(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/file_actions/move/{path}"), "Mock path does not exist")
    def test_move(self):
        path = "foo"
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        file_action.move(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/file_actions/begin_upload/{path}"), "Mock path does not exist")
    def test_begin_upload(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file_action.begin_upload(path, params)

if __name__ == '__main__':
    unittest.main()
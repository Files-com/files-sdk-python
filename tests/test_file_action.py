import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FileAction
from files_sdk import file_action

class FileActionTest(TestBase):
    pass 
    # Instance Methods
    def test_copy(self):
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        file_action = FileAction(params)
        file_action.copy(params)

    def test_move(self):
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        file_action = FileAction(params)
        file_action.move(params)

    def test_begin_upload(self):
        params = {
            "path" : "foo",
        }
        file_action = FileAction(params)
        file_action.begin_upload(params)


    # Static Methods
    def test_copy(self):
        path = "foo"
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        file_action.copy(path, params)

    def test_move(self):
        path = "foo"
        params = {
            "path" : "foo",
            "destination" : "foo",
        }
        file_action.move(path, params)

    def test_begin_upload(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file_action.begin_upload(path, params)

if __name__ == '__main__':
    unittest.main()
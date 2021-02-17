import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import File
from files_sdk import file

class FileTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/files/{path}"), "Mock path does not exist")
    def test_download(self):
        params = {
            "path" : "foo",
        }
        file = File(params)
        file.download(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/files/{path}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "path" : "foo",
        }
        file = File(params)
        file.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/files/{path}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "path" : "foo",
        }
        file = File(params)
        file.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/files/{path}"), "Mock path does not exist")
    def test_download(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file.download(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/files/{path}"), "Mock path does not exist")
    def test_create(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file.create(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/files/{path}"), "Mock path does not exist")
    def test_update(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file.update(path, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/files/{path}"), "Mock path does not exist")
    def test_delete(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file.delete(path, params)

if __name__ == '__main__':
    unittest.main()
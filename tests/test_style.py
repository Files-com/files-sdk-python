import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Style
from files_sdk import style

class StyleTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/styles/{path}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "path" : "foo",
        }
        style = Style(params)
        style.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/styles/{path}"), "Mock path does not exist")
    def test_find(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        style.find(path, params)


    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/styles/{path}"), "Mock path does not exist")
    def test_delete(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        style.delete(path, params)

if __name__ == '__main__':
    unittest.main()
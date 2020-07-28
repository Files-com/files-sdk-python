import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import File
from files_sdk import file

class FileTest(TestBase):
    pass 
    # Instance Methods
    def test_download(self):
        params = {
            "path" : "foo",
        }
        file = File(params)
        file.download(params)

    def test_update(self):
        params = {
            "path" : "foo",
        }
        file = File(params)
        file.update(params)

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
    def test_download(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file.download(path, params)

    def test_create(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file.create(path, params)

    def test_update(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file.update(path, params)

    def test_delete(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        file.delete(path, params)

if __name__ == '__main__':
    unittest.main()
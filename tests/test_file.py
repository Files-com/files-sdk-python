import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import File

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
    def test_do_download(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        File.do_download(path, params)

    def test_do_create(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        File.do_create(path, params)

    def test_do_update(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        File.do_update(path, params)

    def test_do_delete(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        File.do_delete(path, params)

if __name__ == '__main__':
    unittest.main()
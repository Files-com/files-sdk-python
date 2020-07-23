import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Style

class StyleTest(TestBase):
    pass 
    # Instance Methods
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
    def test_do_find(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        Style.do_find(path, params)


    def test_do_delete(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        Style.do_delete(path, params)

if __name__ == '__main__':
    unittest.main()
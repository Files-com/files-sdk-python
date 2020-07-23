import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Folder

class FolderTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        Folder.do_list_for(path, params)

    def test_do_create(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        Folder.do_create(path, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import App

class AppTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        resp = App.do_list()

if __name__ == '__main__':
    unittest.main()
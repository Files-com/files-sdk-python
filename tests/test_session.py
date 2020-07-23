import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Session

class SessionTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_create(self):
        resp = Session.do_create()

    def test_do_delete(self):
        resp = Session.do_delete()

if __name__ == '__main__':
    unittest.main()
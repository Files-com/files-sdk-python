import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Site

class SiteTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_get(self):
        resp = Site.do_get()

    def test_do_get_usage(self):
        resp = Site.do_get_usage()

    def test_do_update(self):
        resp = Site.do_update()

if __name__ == '__main__':
    unittest.main()
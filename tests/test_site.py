import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Site
from files_sdk import site

class SiteTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_get(self):
        resp = site.get()

    def test_get_usage(self):
        resp = site.get_usage()

    def test_update(self):
        resp = site.update()

if __name__ == '__main__':
    unittest.main()
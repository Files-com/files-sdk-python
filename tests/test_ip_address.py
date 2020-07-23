import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import IpAddress

class IpAddressTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        resp = IpAddress.do_list()

    def test_do_get_reserved(self):
        resp = IpAddress.do_get_reserved()

if __name__ == '__main__':
    unittest.main()
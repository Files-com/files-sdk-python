import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import IpAddress
from files_sdk import ip_address

class IpAddressTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        resp = ip_address.list()

    def test_get_reserved(self):
        resp = ip_address.get_reserved()

if __name__ == '__main__':
    unittest.main()
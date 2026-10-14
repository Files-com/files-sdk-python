import unittest
from tests.base import TestBase
from files_sdk import ip_address


class IpAddressTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = ip_address.list()
        self.assert_returns(ip_address.list, result)
        self.assert_typed(result)

    def test_get_smartfile_reserved(self):
        result = ip_address.get_smartfile_reserved()
        self.assert_returns(ip_address.get_smartfile_reserved, result)
        self.assert_typed(result)

    def test_get_exavault_reserved(self):
        result = ip_address.get_exavault_reserved()
        self.assert_returns(ip_address.get_exavault_reserved, result)
        self.assert_typed(result)

    def test_get_reserved(self):
        result = ip_address.get_reserved()
        self.assert_returns(ip_address.get_reserved, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

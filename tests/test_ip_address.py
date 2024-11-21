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
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ip_addresses"), "Mock path does not exist")
    def test_list(self):
        resp = ip_address.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ip_addresses/smartfile-reserved"), "Mock path does not exist")
    def test_get_smartfile_reserved(self):
        resp = ip_address.get_smartfile_reserved()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ip_addresses/exavault-reserved"), "Mock path does not exist")
    def test_get_exavault_reserved(self):
        resp = ip_address.get_exavault_reserved()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ip_addresses/reserved"), "Mock path does not exist")
    def test_get_reserved(self):
        resp = ip_address.get_reserved()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ip_addresses/smartfile-reserved/create_export"), "Mock path does not exist")
    def test_smartfile_reserved_create_export(self):
        resp = ip_address.smartfile_reserved_create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ip_addresses/exavault-reserved/create_export"), "Mock path does not exist")
    def test_exavault_reserved_create_export(self):
        resp = ip_address.exavault_reserved_create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ip_addresses/reserved/create_export"), "Mock path does not exist")
    def test_reserved_create_export(self):
        resp = ip_address.reserved_create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ip_addresses/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = ip_address.create_export()

if __name__ == '__main__':
    unittest.main()
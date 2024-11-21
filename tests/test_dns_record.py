import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import DnsRecord
from files_sdk import dns_record

class DnsRecordTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/dns_records"), "Mock path does not exist")
    def test_list(self):
        resp = dns_record.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/dns_records/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = dns_record.create_export()

if __name__ == '__main__':
    unittest.main()
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
    def test_list(self):
        resp = dns_record.list()

if __name__ == '__main__':
    unittest.main()
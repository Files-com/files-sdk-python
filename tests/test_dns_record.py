import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import DnsRecord

class DnsRecordTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        resp = DnsRecord.do_list()

if __name__ == '__main__':
    unittest.main()
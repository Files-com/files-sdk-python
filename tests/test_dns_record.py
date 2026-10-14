import unittest
from tests.base import TestBase
from files_sdk import dns_record


class DnsRecordTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = dns_record.list()
        self.assert_returns(dns_record.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

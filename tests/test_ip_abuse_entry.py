import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import IpAbuseEntry
from files_sdk import ip_abuse_entry

class IpAbuseEntryTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/ip_abuse_entries"), "Mock path does not exist")
    def test_list(self):
        resp = ip_abuse_entry.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ip_abuse_entries"), "Mock path does not exist")
    def test_create(self):
        params = {
            "ip" : "foo",
        }
        ip_abuse_entry.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/ip_abuse_entries/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = ip_abuse_entry.create_export()

if __name__ == '__main__':
    unittest.main()
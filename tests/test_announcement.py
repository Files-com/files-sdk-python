import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Announcement
from files_sdk import announcement

class AnnouncementTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/announcements"), "Mock path does not exist")
    def test_list(self):
        resp = announcement.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/announcements/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = announcement.create_export()

if __name__ == '__main__':
    unittest.main()
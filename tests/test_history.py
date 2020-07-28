import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import History
from files_sdk import history

class HistoryTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list_for_file(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        history.list_for_file(path, params)

    def test_list_for_folder(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        history.list_for_folder(path, params)

    def test_list_for_user(self):
        user_id = 12345
        params = {
            "user_id" : 12345,
        }
        history.list_for_user(user_id, params)

    def test_list_logins(self):
        resp = history.list_logins()

    def test_list(self):
        resp = history.list()

if __name__ == '__main__':
    unittest.main()
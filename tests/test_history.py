import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import History

class HistoryTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list_for_file(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        History.do_list_for_file(path, params)

    def test_do_list_for_folder(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        History.do_list_for_folder(path, params)

    def test_do_list_for_user(self):
        user_id = 12345
        params = {
            "user_id" : 12345,
        }
        History.do_list_for_user(user_id, params)

    def test_do_list_logins(self):
        resp = History.do_list_logins()

    def test_do_list(self):
        resp = History.do_list()

if __name__ == '__main__':
    unittest.main()
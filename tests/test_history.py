import unittest
from tests.base import TestBase
from files_sdk import history


class HistoryTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list_for_file(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = history.list_for_file(path, params)
        self.assert_returns(history.list_for_file, result)
        self.assert_typed(result)

    def test_list_for_folder(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = history.list_for_folder(path, params)
        self.assert_returns(history.list_for_folder, result)
        self.assert_typed(result)

    def test_list_for_user(self):
        user_id = 12345
        params = {
            "user_id": 12345,
        }
        result = history.list_for_user(user_id, params)
        self.assert_returns(history.list_for_user, result)
        self.assert_typed(result)

    def test_list_logins(self):
        result = history.list_logins()
        self.assert_returns(history.list_logins, result)
        self.assert_typed(result)

    def test_list(self):
        result = history.list()
        self.assert_returns(history.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

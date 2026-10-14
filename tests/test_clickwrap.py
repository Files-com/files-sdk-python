import unittest
from tests.base import TestBase
from files_sdk.models import Clickwrap
from files_sdk import clickwrap


class ClickwrapTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        clickwrap = Clickwrap(params)
        result = clickwrap.update(params)
        self.assert_returns(Clickwrap.update, result)
        self.assert_typed(clickwrap)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        clickwrap = Clickwrap(params)
        clickwrap.delete(params)
        self.assert_typed(clickwrap)

    # Static Methods
    def test_list(self):
        result = clickwrap.list()
        self.assert_returns(clickwrap.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = clickwrap.find(id, params)
        self.assert_returns(clickwrap.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = clickwrap.create()
        self.assert_returns(clickwrap.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = clickwrap.update(id, params)
        self.assert_returns(clickwrap.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = clickwrap.delete(id, params)
        self.assert_returns(clickwrap.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

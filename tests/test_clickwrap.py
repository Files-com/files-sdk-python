import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Clickwrap
from files_sdk import clickwrap

class ClickwrapTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
        }
        clickwrap = Clickwrap(params)
        clickwrap.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        clickwrap = Clickwrap(params)
        clickwrap.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = clickwrap.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        clickwrap.find(id, params)

    def test_create(self):
        resp = clickwrap.create()

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        clickwrap.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        clickwrap.delete(id, params)

if __name__ == '__main__':
    unittest.main()
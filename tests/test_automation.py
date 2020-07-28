import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Automation
from files_sdk import automation

class AutomationTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "automation" : "foo",
        }
        automation = Automation(params)
        automation.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        automation = Automation(params)
        automation.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = automation.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation.find(id, params)

    def test_create(self):
        params = {
            "automation" : "foo",
        }
        automation.create(params)

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "automation" : "foo",
        }
        automation.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        automation.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Automation

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
    def test_do_list(self):
        resp = Automation.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Automation.do_find(id, params)

    def test_do_create(self):
        params = {
            "automation" : "foo",
        }
        Automation.do_create(params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "automation" : "foo",
        }
        Automation.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Automation.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
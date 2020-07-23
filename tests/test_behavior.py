import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Behavior

class BehaviorTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
        }
        behavior = Behavior(params)
        behavior.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        behavior = Behavior(params)
        behavior.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_list(self):
        resp = Behavior.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Behavior.do_find(id, params)

    def test_do_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        Behavior.do_list_for(path, params)

    def test_do_create(self):
        params = {
            "path" : "foo",
            "behavior" : "foo",
        }
        Behavior.do_create(params)

    def test_do_webhook_test(self):
        params = {
            "url" : "foo",
        }
        Behavior.do_webhook_test(params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Behavior.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Behavior.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
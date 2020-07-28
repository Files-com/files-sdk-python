import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Behavior
from files_sdk import behavior

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
    def test_list(self):
        resp = behavior.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        behavior.find(id, params)

    def test_list_for(self):
        path = "foo"
        params = {
            "path" : "foo",
        }
        behavior.list_for(path, params)

    def test_create(self):
        params = {
            "path" : "foo",
            "behavior" : "foo",
        }
        behavior.create(params)

    def test_webhook_test(self):
        params = {
            "url" : "foo",
        }
        behavior.webhook_test(params)

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        behavior.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        behavior.delete(id, params)

if __name__ == '__main__':
    unittest.main()
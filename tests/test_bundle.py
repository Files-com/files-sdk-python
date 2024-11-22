import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Bundle
from files_sdk import bundle

class BundleTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/bundles/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        bundle = Bundle(params)
        bundle.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/bundles/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        bundle = Bundle(params)
        bundle.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bundles"), "Mock path does not exist")
    def test_list(self):
        resp = bundle.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/bundles/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle.find(id, params)



    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/bundles/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/bundles/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        bundle.delete(id, params)

if __name__ == '__main__':
    unittest.main()
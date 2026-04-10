import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import MetadataCategory
from files_sdk import metadata_category

class MetadataCategoryTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/metadata_categories/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        metadata_category = MetadataCategory(params)
        metadata_category.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/metadata_categories/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        metadata_category = MetadataCategory(params)
        metadata_category.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/metadata_categories"), "Mock path does not exist")
    def test_list(self):
        resp = metadata_category.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/metadata_categories/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        metadata_category.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/metadata_categories"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        metadata_category.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/metadata_categories/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        metadata_category.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/metadata_categories/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        metadata_category.delete(id, params)

if __name__ == '__main__':
    unittest.main()
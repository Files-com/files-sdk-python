import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FormFieldSet
from files_sdk import form_field_set

class FormFieldSetTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/form_field_sets/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        form_field_set = FormFieldSet(params)
        form_field_set.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/form_field_sets/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        form_field_set = FormFieldSet(params)
        form_field_set.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/form_field_sets"), "Mock path does not exist")
    def test_list(self):
        resp = form_field_set.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/form_field_sets/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        form_field_set.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/form_field_sets"), "Mock path does not exist")
    def test_create(self):
        resp = form_field_set.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/form_field_sets/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        form_field_set.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/form_field_sets/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        form_field_set.delete(id, params)

if __name__ == '__main__':
    unittest.main()
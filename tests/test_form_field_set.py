import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import FormFieldSet
from files_sdk import form_field_set

class FormFieldSetTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
        }
        form_field_set = FormFieldSet(params)
        form_field_set.update(params)

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
    def test_list(self):
        resp = form_field_set.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        form_field_set.find(id, params)

    def test_create(self):
        resp = form_field_set.create()

    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        form_field_set.update(id, params)

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        form_field_set.delete(id, params)

if __name__ == '__main__':
    unittest.main()
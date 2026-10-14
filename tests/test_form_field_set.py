import unittest
from tests.base import TestBase
from files_sdk.models import FormFieldSet
from files_sdk import form_field_set


class FormFieldSetTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        form_field_set = FormFieldSet(params)
        result = form_field_set.update(params)
        self.assert_returns(FormFieldSet.update, result)
        self.assert_typed(form_field_set)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        form_field_set = FormFieldSet(params)
        form_field_set.delete(params)
        self.assert_typed(form_field_set)

    # Static Methods
    def test_list(self):
        result = form_field_set.list()
        self.assert_returns(form_field_set.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = form_field_set.find(id, params)
        self.assert_returns(form_field_set.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = form_field_set.create()
        self.assert_returns(form_field_set.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = form_field_set.update(id, params)
        self.assert_returns(form_field_set.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = form_field_set.delete(id, params)
        self.assert_returns(form_field_set.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

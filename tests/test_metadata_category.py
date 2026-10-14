import unittest
from tests.base import TestBase
from files_sdk.models import MetadataCategory
from files_sdk import metadata_category


class MetadataCategoryTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        metadata_category = MetadataCategory(params)
        result = metadata_category.update(params)
        self.assert_returns(MetadataCategory.update, result)
        self.assert_typed(metadata_category)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        metadata_category = MetadataCategory(params)
        metadata_category.delete(params)
        self.assert_typed(metadata_category)

    # Static Methods
    def test_list(self):
        result = metadata_category.list()
        self.assert_returns(metadata_category.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = metadata_category.find(id, params)
        self.assert_returns(metadata_category.find, result)
        self.assert_typed(result)

    def test_list_for(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = metadata_category.list_for(path, params)
        self.assert_returns(metadata_category.list_for, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
        }
        result = metadata_category.create(params)
        self.assert_returns(metadata_category.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = metadata_category.update(id, params)
        self.assert_returns(metadata_category.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = metadata_category.delete(id, params)
        self.assert_returns(metadata_category.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

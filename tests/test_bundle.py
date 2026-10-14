import unittest
from tests.base import TestBase
from files_sdk.models import Bundle
from files_sdk import bundle


class BundleTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        bundle = Bundle(params)
        result = bundle.update(params)
        self.assert_returns(Bundle.update, result)
        self.assert_typed(bundle)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        bundle = Bundle(params)
        bundle.delete(params)
        self.assert_typed(bundle)

    # Static Methods
    def test_list(self):
        result = bundle.list()
        self.assert_returns(bundle.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = bundle.find(id, params)
        self.assert_returns(bundle.find, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = bundle.update(id, params)
        self.assert_returns(bundle.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = bundle.delete(id, params)
        self.assert_returns(bundle.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

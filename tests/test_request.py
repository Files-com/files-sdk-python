import unittest
from tests.base import TestBase
from files_sdk.models import Request
from files_sdk import request


class RequestTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        request = Request(params)
        request.delete(params)
        self.assert_typed(request)

    # Static Methods
    def test_list(self):
        result = request.list()
        self.assert_returns(request.list, result)
        self.assert_typed(result)

    def test_get_folder(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = request.get_folder(path, params)
        self.assert_returns(request.get_folder, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "path": "foo",
            "destination": "foo",
        }
        result = request.create(params)
        self.assert_returns(request.create, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = request.delete(id, params)
        self.assert_returns(request.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

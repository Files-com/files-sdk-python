import unittest
from tests.base import TestBase
from files_sdk.models import UserRequest
from files_sdk import user_request


class UserRequestTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        user_request = UserRequest(params)
        user_request.delete(params)
        self.assert_typed(user_request)

    # Static Methods
    def test_list(self):
        result = user_request.list()
        self.assert_returns(user_request.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_request.find(id, params)
        self.assert_returns(user_request.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "email": "foo",
            "details": "foo",
        }
        result = user_request.create(params)
        self.assert_returns(user_request.create, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_request.delete(id, params)
        self.assert_returns(user_request.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

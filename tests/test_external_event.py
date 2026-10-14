import unittest
from tests.base import TestBase
from files_sdk import external_event


class ExternalEventTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = external_event.list()
        self.assert_returns(external_event.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = external_event.find(id, params)
        self.assert_returns(external_event.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "status": "foo",
            "body": "foo",
        }
        result = external_event.create(params)
        self.assert_returns(external_event.create, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

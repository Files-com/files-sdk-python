import unittest
from tests.base import TestBase
from files_sdk.models import DatabaseDestination
from files_sdk import database_destination


class DatabaseDestinationTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        database_destination = DatabaseDestination(params)
        result = database_destination.update(params)
        self.assert_returns(DatabaseDestination.update, result)
        self.assert_typed(database_destination)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        database_destination = DatabaseDestination(params)
        database_destination.delete(params)
        self.assert_typed(database_destination)

    # Static Methods
    def test_list(self):
        result = database_destination.list()
        self.assert_returns(database_destination.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = database_destination.find(id, params)
        self.assert_returns(database_destination.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "provider": "foo",
            "config": {},
            "secret_id": 12345,
        }
        result = database_destination.create(params)
        self.assert_returns(database_destination.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = database_destination.update(id, params)
        self.assert_returns(database_destination.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = database_destination.delete(id, params)
        self.assert_returns(database_destination.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

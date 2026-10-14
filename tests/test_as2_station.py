import unittest
from tests.base import TestBase
from files_sdk.models import As2Station
from files_sdk import as2_station


class As2StationTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        as2_station = As2Station(params)
        result = as2_station.update(params)
        self.assert_returns(As2Station.update, result)
        self.assert_typed(as2_station)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        as2_station = As2Station(params)
        as2_station.delete(params)
        self.assert_typed(as2_station)

    # Static Methods
    def test_list(self):
        result = as2_station.list()
        self.assert_returns(as2_station.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = as2_station.find(id, params)
        self.assert_returns(as2_station.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
        }
        result = as2_station.create(params)
        self.assert_returns(as2_station.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = as2_station.update(id, params)
        self.assert_returns(as2_station.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = as2_station.delete(id, params)
        self.assert_returns(as2_station.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

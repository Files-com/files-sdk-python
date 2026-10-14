import unittest
from tests.base import TestBase
from files_sdk.models import SiemHttpDestination
from files_sdk import siem_http_destination


class SiemHttpDestinationTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        siem_http_destination = SiemHttpDestination(params)
        result = siem_http_destination.update(params)
        self.assert_returns(SiemHttpDestination.update, result)
        self.assert_typed(siem_http_destination)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        siem_http_destination = SiemHttpDestination(params)
        siem_http_destination.delete(params)
        self.assert_typed(siem_http_destination)

    # Static Methods
    def test_list(self):
        result = siem_http_destination.list()
        self.assert_returns(siem_http_destination.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = siem_http_destination.find(id, params)
        self.assert_returns(siem_http_destination.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "destination_type": "foo",
        }
        result = siem_http_destination.create(params)
        self.assert_returns(siem_http_destination.create, result)
        self.assert_typed(result)

    def test_send_test_entry(self):
        result = siem_http_destination.send_test_entry()
        self.assert_returns(siem_http_destination.send_test_entry, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = siem_http_destination.update(id, params)
        self.assert_returns(siem_http_destination.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = siem_http_destination.delete(id, params)
        self.assert_returns(siem_http_destination.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

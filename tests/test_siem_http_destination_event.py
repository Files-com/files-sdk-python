import unittest
from tests.base import TestBase
from files_sdk import siem_http_destination_event


class SiemHttpDestinationEventTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = siem_http_destination_event.list()
        self.assert_returns(siem_http_destination_event.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = siem_http_destination_event.find(id, params)
        self.assert_returns(siem_http_destination_event.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

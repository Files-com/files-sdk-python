import unittest
from tests.base import TestBase
from files_sdk.models import ExpectationIncident
from files_sdk import expectation_incident


class ExpectationIncidentTest(TestBase):
    # Instance Methods
    def test_instance_resolve(self):
        params = {
            "id": 12345,
        }
        expectation_incident = ExpectationIncident(params)
        result = expectation_incident.resolve(params)
        self.assert_returns(ExpectationIncident.resolve, result)
        self.assert_typed(expectation_incident)

    def test_instance_snooze(self):
        params = {
            "id": 12345,
            "snoozed_until": "foo",
        }
        expectation_incident = ExpectationIncident(params)
        result = expectation_incident.snooze(params)
        self.assert_returns(ExpectationIncident.snooze, result)
        self.assert_typed(expectation_incident)

    def test_instance_acknowledge(self):
        params = {
            "id": 12345,
        }
        expectation_incident = ExpectationIncident(params)
        result = expectation_incident.acknowledge(params)
        self.assert_returns(ExpectationIncident.acknowledge, result)
        self.assert_typed(expectation_incident)

    # Static Methods
    def test_list(self):
        result = expectation_incident.list()
        self.assert_returns(expectation_incident.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = expectation_incident.find(id, params)
        self.assert_returns(expectation_incident.find, result)
        self.assert_typed(result)

    def test_resolve(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = expectation_incident.resolve(id, params)
        self.assert_returns(expectation_incident.resolve, result)
        self.assert_typed(result)

    def test_snooze(self):
        id = 12345
        params = {
            "id": 12345,
            "snoozed_until": "foo",
        }
        result = expectation_incident.snooze(id, params)
        self.assert_returns(expectation_incident.snooze, result)
        self.assert_typed(result)

    def test_acknowledge(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = expectation_incident.acknowledge(id, params)
        self.assert_returns(expectation_incident.acknowledge, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

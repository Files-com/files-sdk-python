import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import ExpectationIncident
from files_sdk import expectation_incident

class ExpectationIncidentTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectation_incidents/{id}/resolve"), "Mock path does not exist")
    def test_resolve(self):
        params = {
            "id" : 12345,
        }
        expectation_incident = ExpectationIncident(params)
        expectation_incident.resolve(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectation_incidents/{id}/snooze"), "Mock path does not exist")
    def test_snooze(self):
        params = {
            "id" : 12345,
            "snoozed_until" : "foo",
        }
        expectation_incident = ExpectationIncident(params)
        expectation_incident.snooze(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectation_incidents/{id}/acknowledge"), "Mock path does not exist")
    def test_acknowledge(self):
        params = {
            "id" : 12345,
        }
        expectation_incident = ExpectationIncident(params)
        expectation_incident.acknowledge(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/expectation_incidents"), "Mock path does not exist")
    def test_list(self):
        resp = expectation_incident.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/expectation_incidents/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        expectation_incident.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectation_incidents/{id}/resolve"), "Mock path does not exist")
    def test_resolve(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        expectation_incident.resolve(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectation_incidents/{id}/snooze"), "Mock path does not exist")
    def test_snooze(self):
        id = 12345
        params = {
            "id" : 12345,
            "snoozed_until" : "foo",
        }
        expectation_incident.snooze(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/expectation_incidents/{id}/acknowledge"), "Mock path does not exist")
    def test_acknowledge(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        expectation_incident.acknowledge(id, params)

if __name__ == '__main__':
    unittest.main()
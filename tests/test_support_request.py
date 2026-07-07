import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import SupportRequest
from files_sdk import support_request

class SupportRequestTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/support_requests/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        support_request = SupportRequest(params)
        support_request.update(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/support_requests"), "Mock path does not exist")
    def test_list(self):
        resp = support_request.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/support_requests"), "Mock path does not exist")
    def test_create(self):
        params = {
            "email" : "foo",
            "subject" : "foo",
            "comment" : "foo",
        }
        support_request.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/support_requests/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = support_request.create_export()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/support_requests/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        support_request.update(id, params)

if __name__ == '__main__':
    unittest.main()
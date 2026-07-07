import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import NpsResponse
from files_sdk import nps_response

class NpsResponseTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/nps_responses/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
            "comment" : "foo",
        }
        nps_response = NpsResponse(params)
        nps_response.update(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/nps_responses"), "Mock path does not exist")
    def test_create(self):
        resp = nps_response.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/nps_responses/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "comment" : "foo",
        }
        nps_response.update(id, params)

if __name__ == '__main__':
    unittest.main()
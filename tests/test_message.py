import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Message
from files_sdk import message

class MessageTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/messages/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
            "project_id" : 12345,
            "subject" : "foo",
            "body" : "foo",
        }
        message = Message(params)
        message.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/messages/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        message = Message(params)
        message.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/messages"), "Mock path does not exist")
    def test_list(self):
        params = {
            "project_id" : 12345,
        }
        message.list(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/messages/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        message.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/messages"), "Mock path does not exist")
    def test_create(self):
        params = {
            "project_id" : 12345,
            "subject" : "foo",
            "body" : "foo",
        }
        message.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/messages/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "project_id" : 12345,
            "subject" : "foo",
            "body" : "foo",
        }
        message.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/messages/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        message.delete(id, params)

if __name__ == '__main__':
    unittest.main()
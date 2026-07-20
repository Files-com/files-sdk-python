import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import UserAdditionalEmailRecipient
from files_sdk import user_additional_email_recipient

class UserAdditionalEmailRecipientTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/user_additional_email_recipients/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        user_additional_email_recipient = UserAdditionalEmailRecipient(params)
        user_additional_email_recipient.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/user_additional_email_recipients/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        user_additional_email_recipient = UserAdditionalEmailRecipient(params)
        user_additional_email_recipient.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/user_additional_email_recipients"), "Mock path does not exist")
    def test_list(self):
        resp = user_additional_email_recipient.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/user_additional_email_recipients/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user_additional_email_recipient.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/user_additional_email_recipients"), "Mock path does not exist")
    def test_create(self):
        params = {
            "email" : "foo",
        }
        user_additional_email_recipient.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/user_additional_email_recipients/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user_additional_email_recipient.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/user_additional_email_recipients/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        user_additional_email_recipient.delete(id, params)

if __name__ == '__main__':
    unittest.main()
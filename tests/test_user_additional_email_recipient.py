import unittest
from tests.base import TestBase
from files_sdk.models import UserAdditionalEmailRecipient
from files_sdk import user_additional_email_recipient


class UserAdditionalEmailRecipientTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        user_additional_email_recipient = UserAdditionalEmailRecipient(params)
        result = user_additional_email_recipient.update(params)
        self.assert_returns(UserAdditionalEmailRecipient.update, result)
        self.assert_typed(user_additional_email_recipient)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        user_additional_email_recipient = UserAdditionalEmailRecipient(params)
        user_additional_email_recipient.delete(params)
        self.assert_typed(user_additional_email_recipient)

    # Static Methods
    def test_list(self):
        result = user_additional_email_recipient.list()
        self.assert_returns(user_additional_email_recipient.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_additional_email_recipient.find(id, params)
        self.assert_returns(user_additional_email_recipient.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "email": "foo",
        }
        result = user_additional_email_recipient.create(params)
        self.assert_returns(user_additional_email_recipient.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_additional_email_recipient.update(id, params)
        self.assert_returns(user_additional_email_recipient.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = user_additional_email_recipient.delete(id, params)
        self.assert_returns(user_additional_email_recipient.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

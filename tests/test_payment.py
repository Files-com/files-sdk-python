import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Payment
from files_sdk import payment

class PaymentTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/payments"), "Mock path does not exist")
    def test_list(self):
        resp = payment.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/payments/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        payment.find(id, params)

if __name__ == '__main__':
    unittest.main()
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
    def test_list(self):
        resp = payment.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        payment.find(id, params)

if __name__ == '__main__':
    unittest.main()
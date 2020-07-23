import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Payment

class PaymentTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        resp = Payment.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Payment.do_find(id, params)

if __name__ == '__main__':
    unittest.main()
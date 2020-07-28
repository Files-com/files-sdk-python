import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Invoice
from files_sdk import invoice

class InvoiceTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_list(self):
        resp = invoice.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        invoice.find(id, params)

if __name__ == '__main__':
    unittest.main()
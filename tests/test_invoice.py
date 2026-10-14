import unittest
from tests.base import TestBase
from files_sdk import invoice


class InvoiceTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = invoice.list()
        self.assert_returns(invoice.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = invoice.find(id, params)
        self.assert_returns(invoice.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

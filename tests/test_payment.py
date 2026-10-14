import unittest
from tests.base import TestBase
from files_sdk import payment


class PaymentTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = payment.list()
        self.assert_returns(payment.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = payment.find(id, params)
        self.assert_returns(payment.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

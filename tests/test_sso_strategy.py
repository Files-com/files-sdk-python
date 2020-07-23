import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import SsoStrategy

class SsoStrategyTest(TestBase):
    pass 
    # Instance Methods

    # Static Methods
    def test_do_list(self):
        resp = SsoStrategy.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        SsoStrategy.do_find(id, params)

if __name__ == '__main__':
    unittest.main()
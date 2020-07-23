import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import As2Key

class As2KeyTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "as2_partnership_name" : "foo",
        }
        as2_key = As2Key(params)
        as2_key.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        as2_key = As2Key(params)
        as2_key.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_list(self):
        resp = As2Key.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        As2Key.do_find(id, params)

    def test_do_create(self):
        params = {
            "as2_partnership_name" : "foo",
            "public_key" : "foo",
        }
        As2Key.do_create(params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "as2_partnership_name" : "foo",
        }
        As2Key.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        As2Key.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
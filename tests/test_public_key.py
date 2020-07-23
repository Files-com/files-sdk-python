import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import PublicKey

class PublicKeyTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "title" : "foo",
        }
        public_key = PublicKey(params)
        public_key.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        public_key = PublicKey(params)
        public_key.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_list(self):
        resp = PublicKey.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        PublicKey.do_find(id, params)

    def test_do_create(self):
        params = {
            "title" : "foo",
            "public_key" : "foo",
        }
        PublicKey.do_create(params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "title" : "foo",
        }
        PublicKey.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        PublicKey.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
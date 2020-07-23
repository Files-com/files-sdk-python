import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Message

class MessageTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
            "project_id" : 12345,
            "subject" : "foo",
            "body" : "foo",
        }
        message = Message(params)
        message.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        message = Message(params)
        message.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_list(self):
        params = {
            "project_id" : 12345,
        }
        Message.do_list(params)

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Message.do_find(id, params)

    def test_do_create(self):
        params = {
            "project_id" : 12345,
            "subject" : "foo",
            "body" : "foo",
        }
        Message.do_create(params)

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
            "project_id" : 12345,
            "subject" : "foo",
            "body" : "foo",
        }
        Message.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Message.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
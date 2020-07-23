import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import Notification

class NotificationTest(TestBase):
    pass 
    # Instance Methods
    def test_update(self):
        params = {
            "id" : 12345,
        }
        notification = Notification(params)
        notification.update(params)

    def test_delete(self):
        params = {
            "id" : 12345,
        }
        notification = Notification(params)
        notification.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_do_list(self):
        resp = Notification.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Notification.do_find(id, params)

    def test_do_create(self):
        resp = Notification.do_create()

    def test_do_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Notification.do_update(id, params)

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        Notification.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Sync
from files_sdk import sync

class SyncTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/syncs/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        sync = Sync(params)
        sync.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/syncs/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        sync = Sync(params)
        sync.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/syncs"), "Mock path does not exist")
    def test_list(self):
        resp = sync.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/syncs/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sync.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/syncs"), "Mock path does not exist")
    def test_create(self):
        resp = sync.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/syncs/migrate_to_syncs"), "Mock path does not exist")
    def test_create_migrate_to(self):
        resp = sync.create_migrate_to()

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/syncs/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sync.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/syncs/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        sync.delete(id, params)

if __name__ == '__main__':
    unittest.main()
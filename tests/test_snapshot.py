import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Snapshot
from files_sdk import snapshot

class SnapshotTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/snapshots/{id}/finalize"), "Mock path does not exist")
    def test_finalize(self):
        params = {
            "id" : 12345,
        }
        snapshot = Snapshot(params)
        snapshot.finalize(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/snapshots/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        snapshot = Snapshot(params)
        snapshot.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/snapshots/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        snapshot = Snapshot(params)
        snapshot.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/snapshots"), "Mock path does not exist")
    def test_list(self):
        resp = snapshot.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/snapshots/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        snapshot.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/snapshots"), "Mock path does not exist")
    def test_create(self):
        resp = snapshot.create()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/snapshots/{id}/finalize"), "Mock path does not exist")
    def test_finalize(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        snapshot.finalize(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/snapshots/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        snapshot.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/snapshots/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        snapshot.delete(id, params)

if __name__ == '__main__':
    unittest.main()
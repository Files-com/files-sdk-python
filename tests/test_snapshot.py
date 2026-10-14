import unittest
from tests.base import TestBase
from files_sdk.models import Snapshot
from files_sdk import snapshot


class SnapshotTest(TestBase):
    # Instance Methods
    def test_instance_finalize(self):
        params = {
            "id": 12345,
        }
        snapshot = Snapshot(params)
        snapshot.finalize(params)
        self.assert_typed(snapshot)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        snapshot = Snapshot(params)
        result = snapshot.update(params)
        self.assert_returns(Snapshot.update, result)
        self.assert_typed(snapshot)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        snapshot = Snapshot(params)
        snapshot.delete(params)
        self.assert_typed(snapshot)

    # Static Methods
    def test_list(self):
        result = snapshot.list()
        self.assert_returns(snapshot.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = snapshot.find(id, params)
        self.assert_returns(snapshot.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = snapshot.create()
        self.assert_returns(snapshot.create, result)
        self.assert_typed(result)

    def test_finalize(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = snapshot.finalize(id, params)
        self.assert_returns(snapshot.finalize, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = snapshot.update(id, params)
        self.assert_returns(snapshot.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = snapshot.delete(id, params)
        self.assert_returns(snapshot.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

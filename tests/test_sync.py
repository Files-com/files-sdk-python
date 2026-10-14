import unittest
from tests.base import TestBase
from files_sdk.models import Sync
from files_sdk import sync


class SyncTest(TestBase):
    # Instance Methods
    def test_instance_dry_run(self):
        params = {
            "id": 12345,
        }
        sync = Sync(params)
        sync.dry_run(params)
        self.assert_typed(sync)

    def test_instance_manual_run(self):
        params = {
            "id": 12345,
        }
        sync = Sync(params)
        sync.manual_run(params)
        self.assert_typed(sync)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        sync = Sync(params)
        result = sync.update(params)
        self.assert_returns(Sync.update, result)
        self.assert_typed(sync)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        sync = Sync(params)
        sync.delete(params)
        self.assert_typed(sync)

    # Static Methods
    def test_list(self):
        result = sync.list()
        self.assert_returns(sync.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sync.find(id, params)
        self.assert_returns(sync.find, result)
        self.assert_typed(result)

    def test_create(self):
        result = sync.create()
        self.assert_returns(sync.create, result)
        self.assert_typed(result)

    def test_dry_run(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sync.dry_run(id, params)
        self.assert_returns(sync.dry_run, result)
        self.assert_typed(result)

    def test_manual_run(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sync.manual_run(id, params)
        self.assert_returns(sync.manual_run, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sync.update(id, params)
        self.assert_returns(sync.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = sync.delete(id, params)
        self.assert_returns(sync.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

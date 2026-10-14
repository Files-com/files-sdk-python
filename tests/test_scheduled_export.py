import unittest
from tests.base import TestBase
from files_sdk.models import ScheduledExport
from files_sdk import scheduled_export


class ScheduledExportTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        scheduled_export = ScheduledExport(params)
        result = scheduled_export.update(params)
        self.assert_returns(ScheduledExport.update, result)
        self.assert_typed(scheduled_export)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        scheduled_export = ScheduledExport(params)
        scheduled_export.delete(params)
        self.assert_typed(scheduled_export)

    # Static Methods
    def test_list(self):
        result = scheduled_export.list()
        self.assert_returns(scheduled_export.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = scheduled_export.find(id, params)
        self.assert_returns(scheduled_export.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "export_type": "foo",
        }
        result = scheduled_export.create(params)
        self.assert_returns(scheduled_export.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = scheduled_export.update(id, params)
        self.assert_returns(scheduled_export.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = scheduled_export.delete(id, params)
        self.assert_returns(scheduled_export.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

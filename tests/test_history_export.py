import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import HistoryExport
from files_sdk import history_export

class HistoryExportTest(TestBase):
    pass 
    # Instance Methods
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        history_export = HistoryExport(params)
        history_export.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    def test_list(self):
        resp = history_export.list()

    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        history_export.find(id, params)

    def test_create(self):
        resp = history_export.create()

    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        history_export.delete(id, params)

if __name__ == '__main__':
    unittest.main()
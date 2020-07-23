import unittest
import inspect
import files_com
from tests.base import TestBase
from files_com import HistoryExport

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
    def test_do_list(self):
        resp = HistoryExport.do_list()

    def test_do_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        HistoryExport.do_find(id, params)

    def test_do_create(self):
        resp = HistoryExport.do_create()

    def test_do_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        HistoryExport.do_delete(id, params)

if __name__ == '__main__':
    unittest.main()
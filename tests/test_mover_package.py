import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import MoverPackage
from files_sdk import mover_package

class MoverPackageTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/mover_packages/{id}/purchase"), "Mock path does not exist")
    def test_purchase(self):
        params = {
            "id" : 12345,
        }
        mover_package = MoverPackage(params)
        mover_package.purchase(params)


    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/mover_packages"), "Mock path does not exist")
    def test_list(self):
        resp = mover_package.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/mover_packages/{id}/purchase"), "Mock path does not exist")
    def test_purchase(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        mover_package.purchase(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/mover_packages/create_export"), "Mock path does not exist")
    def test_create_export(self):
        resp = mover_package.create_export()

if __name__ == '__main__':
    unittest.main()
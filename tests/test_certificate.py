import unittest
from tests.base import TestBase
from files_sdk.models import Certificate
from files_sdk import certificate


class CertificateTest(TestBase):
    # Instance Methods
    def test_instance_activate(self):
        params = {
            "id": 12345,
        }
        certificate = Certificate(params)
        certificate.activate(params)
        self.assert_typed(certificate)

    def test_instance_deactivate(self):
        params = {
            "id": 12345,
        }
        certificate = Certificate(params)
        certificate.deactivate(params)
        self.assert_typed(certificate)

    def test_instance_replace_with_files(self):
        params = {
            "id": 12345,
        }
        certificate = Certificate(params)
        certificate.replace_with_files(params)
        self.assert_typed(certificate)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        certificate = Certificate(params)
        result = certificate.update(params)
        self.assert_returns(Certificate.update, result)
        self.assert_typed(certificate)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        certificate = Certificate(params)
        certificate.delete(params)
        self.assert_typed(certificate)

    # Static Methods
    def test_list(self):
        result = certificate.list()
        self.assert_returns(certificate.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = certificate.find(id, params)
        self.assert_returns(certificate.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
        }
        result = certificate.create(params)
        self.assert_returns(certificate.create, result)
        self.assert_typed(result)

    def test_activate(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = certificate.activate(id, params)
        self.assert_returns(certificate.activate, result)
        self.assert_typed(result)

    def test_deactivate(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = certificate.deactivate(id, params)
        self.assert_returns(certificate.deactivate, result)
        self.assert_typed(result)

    def test_replace_with_files(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = certificate.replace_with_files(id, params)
        self.assert_returns(certificate.replace_with_files, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = certificate.update(id, params)
        self.assert_returns(certificate.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = certificate.delete(id, params)
        self.assert_returns(certificate.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

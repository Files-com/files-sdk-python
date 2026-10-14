import unittest
from tests.base import TestBase
from files_sdk.models import File
from files_sdk import file


class FileTest(TestBase):
    # Instance Methods
    def test_instance_download(self):
        params = {
            "path": "foo",
        }
        file = File(params)
        result = file.download(params)
        self.assert_returns(File.download, result)
        self.assert_typed(file)

    def test_instance_update(self):
        params = {
            "path": "foo",
        }
        file = File(params)
        result = file.update(params)
        self.assert_returns(File.update, result)
        self.assert_typed(file)

    def test_instance_delete(self):
        params = {
            "path": "foo",
        }
        file = File(params)
        file.delete(params)
        self.assert_typed(file)

    def test_instance_zip_list_contents(self):
        params = {
            "path": "foo",
        }
        file = File(params)
        result = file.zip_list_contents(params)
        self.assert_returns(File.zip_list_contents, result)
        self.assert_typed(file)

    def test_instance_begin_delete(self):
        params = {
            "path": "foo",
        }
        file = File(params)
        result = file.begin_delete(params)
        self.assert_returns(File.begin_delete, result)
        self.assert_typed(file)

    def test_instance_copy(self):
        params = {
            "path": "foo",
            "destination": "foo",
        }
        file = File(params)
        result = file.copy(params)
        self.assert_returns(File.copy, result)
        self.assert_typed(file)

    def test_instance_move(self):
        params = {
            "path": "foo",
            "destination": "foo",
        }
        file = File(params)
        result = file.move(params)
        self.assert_returns(File.move, result)
        self.assert_typed(file)

    def test_instance_transform(self):
        params = {
            "path": "foo",
            "destination": "foo",
            "transform_type": "foo",
            "target_format": "foo",
        }
        file = File(params)
        result = file.transform(params)
        self.assert_returns(File.transform, result)
        self.assert_typed(file)

    def test_instance_gpg_decrypt(self):
        params = {
            "path": "foo",
            "destination": "foo",
        }
        file = File(params)
        result = file.gpg_decrypt(params)
        self.assert_returns(File.gpg_decrypt, result)
        self.assert_typed(file)

    def test_instance_gpg_encrypt(self):
        params = {
            "path": "foo",
            "destination": "foo",
        }
        file = File(params)
        result = file.gpg_encrypt(params)
        self.assert_returns(File.gpg_encrypt, result)
        self.assert_typed(file)

    def test_instance_unzip(self):
        params = {
            "path": "foo",
            "destination": "foo",
        }
        file = File(params)
        result = file.unzip(params)
        self.assert_returns(File.unzip, result)
        self.assert_typed(file)

    def test_instance_begin_upload(self):
        params = {
            "path": "foo",
        }
        file = File(params)
        result = file.begin_upload(params)
        self.assert_returns(File.begin_upload, result)
        self.assert_typed(file)

    # Static Methods
    def test_download(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file.download(path, params)
        self.assert_returns(file.download, result)
        self.assert_typed(result)

    def test_create(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file.create(path, params)
        self.assert_returns(file.create, result)
        self.assert_typed(result)

    def test_update(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file.update(path, params)
        self.assert_returns(file.update, result)
        self.assert_typed(result)

    def test_delete(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file.delete(path, params)
        self.assert_returns(file.delete, result)
        self.assert_typed(result)

    def test_find(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file.find(path, params)
        self.assert_returns(file.find, result)
        self.assert_typed(result)

    def test_zip_list_contents(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file.zip_list_contents(path, params)
        self.assert_returns(file.zip_list_contents, result)
        self.assert_typed(result)

    def test_begin_delete(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file.begin_delete(path, params)
        self.assert_returns(file.begin_delete, result)
        self.assert_typed(result)

    def test_copy(self):
        path = "foo"
        params = {
            "path": "foo",
            "destination": "foo",
        }
        result = file.copy(path, params)
        self.assert_returns(file.copy, result)
        self.assert_typed(result)

    def test_move(self):
        path = "foo"
        params = {
            "path": "foo",
            "destination": "foo",
        }
        result = file.move(path, params)
        self.assert_returns(file.move, result)
        self.assert_typed(result)

    def test_transform(self):
        path = "foo"
        params = {
            "path": "foo",
            "destination": "foo",
            "transform_type": "foo",
            "target_format": "foo",
        }
        result = file.transform(path, params)
        self.assert_returns(file.transform, result)
        self.assert_typed(result)

    def test_gpg_decrypt(self):
        path = "foo"
        params = {
            "path": "foo",
            "destination": "foo",
        }
        result = file.gpg_decrypt(path, params)
        self.assert_returns(file.gpg_decrypt, result)
        self.assert_typed(result)

    def test_gpg_encrypt(self):
        path = "foo"
        params = {
            "path": "foo",
            "destination": "foo",
        }
        result = file.gpg_encrypt(path, params)
        self.assert_returns(file.gpg_encrypt, result)
        self.assert_typed(result)

    def test_unzip(self):
        path = "foo"
        params = {
            "path": "foo",
            "destination": "foo",
        }
        result = file.unzip(path, params)
        self.assert_returns(file.unzip, result)
        self.assert_typed(result)

    def test_zip(self):
        params = {
            "paths": ["foo1"],
            "destination": "foo",
        }
        result = file.zip(params)
        self.assert_returns(file.zip, result)
        self.assert_typed(result)

    def test_begin_upload(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = file.begin_upload(path, params)
        self.assert_returns(file.begin_upload, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

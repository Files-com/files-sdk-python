import unittest
from tests.base import TestBase
from files_sdk import folder


class FolderTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list_for(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = folder.list_for(path, params)
        self.assert_returns(folder.list_for, result)
        self.assert_typed(result)

    def test_create(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = folder.create(path, params)
        self.assert_returns(folder.create, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

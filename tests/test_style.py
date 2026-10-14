import unittest
from tests.base import TestBase
from files_sdk.models import Style
from files_sdk import style


class StyleTest(TestBase):
    # Instance Methods
    def test_instance_delete(self):
        params = {
            "path": "foo",
        }
        style = Style(params)
        style.delete(params)
        self.assert_typed(style)

    # Static Methods
    def test_find(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = style.find(path, params)
        self.assert_returns(style.find, result)
        self.assert_typed(result)

    def test_delete(self):
        path = "foo"
        params = {
            "path": "foo",
        }
        result = style.delete(path, params)
        self.assert_returns(style.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

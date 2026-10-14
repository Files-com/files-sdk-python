import unittest
from tests.base import TestBase
from files_sdk import scim_log


class ScimLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = scim_log.list()
        self.assert_returns(scim_log.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = scim_log.find(id, params)
        self.assert_returns(scim_log.find, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

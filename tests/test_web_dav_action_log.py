import unittest
from tests.base import TestBase
from files_sdk import web_dav_action_log


class WebDavActionLogTest(TestBase):
    # Instance Methods

    # Static Methods
    def test_list(self):
        result = web_dav_action_log.list()
        self.assert_returns(web_dav_action_log.list, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

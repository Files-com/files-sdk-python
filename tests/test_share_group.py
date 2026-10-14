import unittest
from tests.base import TestBase
from files_sdk.models import ShareGroup
from files_sdk import share_group


class ShareGroupTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        share_group = ShareGroup(params)
        result = share_group.update(params)
        self.assert_returns(ShareGroup.update, result)
        self.assert_typed(share_group)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        share_group = ShareGroup(params)
        share_group.delete(params)
        self.assert_typed(share_group)

    # Static Methods
    def test_list(self):
        result = share_group.list()
        self.assert_returns(share_group.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = share_group.find(id, params)
        self.assert_returns(share_group.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "members": [{}],
        }
        result = share_group.create(params)
        self.assert_returns(share_group.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = share_group.update(id, params)
        self.assert_returns(share_group.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = share_group.delete(id, params)
        self.assert_returns(share_group.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

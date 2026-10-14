import unittest
from tests.base import TestBase
from files_sdk.models import EventTarget
from files_sdk import event_target


class EventTargetTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        event_target = EventTarget(params)
        result = event_target.update(params)
        self.assert_returns(EventTarget.update, result)
        self.assert_typed(event_target)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        event_target = EventTarget(params)
        event_target.delete(params)
        self.assert_typed(event_target)

    # Static Methods
    def test_list(self):
        result = event_target.list()
        self.assert_returns(event_target.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_target.find(id, params)
        self.assert_returns(event_target.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "config": {},
            "target_type": "foo",
        }
        result = event_target.create(params)
        self.assert_returns(event_target.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_target.update(id, params)
        self.assert_returns(event_target.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = event_target.delete(id, params)
        self.assert_returns(event_target.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

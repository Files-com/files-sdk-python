import unittest
from tests.base import TestBase
from files_sdk.models import AiTask
from files_sdk import ai_task


class AiTaskTest(TestBase):
    # Instance Methods
    def test_instance_manual_run(self):
        params = {
            "id": 12345,
        }
        ai_task = AiTask(params)
        ai_task.manual_run(params)
        self.assert_typed(ai_task)

    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        ai_task = AiTask(params)
        result = ai_task.update(params)
        self.assert_returns(AiTask.update, result)
        self.assert_typed(ai_task)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        ai_task = AiTask(params)
        ai_task.delete(params)
        self.assert_typed(ai_task)

    # Static Methods
    def test_list(self):
        result = ai_task.list()
        self.assert_returns(ai_task.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = ai_task.find(id, params)
        self.assert_returns(ai_task.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "prompt": "foo",
        }
        result = ai_task.create(params)
        self.assert_returns(ai_task.create, result)
        self.assert_typed(result)

    def test_manual_run(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = ai_task.manual_run(id, params)
        self.assert_returns(ai_task.manual_run, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = ai_task.update(id, params)
        self.assert_returns(ai_task.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = ai_task.delete(id, params)
        self.assert_returns(ai_task.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

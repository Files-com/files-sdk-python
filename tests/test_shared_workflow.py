import unittest
from tests.base import TestBase
from files_sdk.models import SharedWorkflow
from files_sdk import shared_workflow


class SharedWorkflowTest(TestBase):
    # Instance Methods
    def test_instance_run_workflow(self):
        params = {
            "id": 12345,
            "submission_revision": "foo",
            "submission_id": "foo",
            "file_path": "foo",
        }
        shared_workflow = SharedWorkflow(params)
        result = shared_workflow.run_workflow(params)
        self.assert_returns(SharedWorkflow.run_workflow, result)
        self.assert_typed(shared_workflow)

    # Static Methods
    def test_list(self):
        result = shared_workflow.list()
        self.assert_returns(shared_workflow.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = shared_workflow.find(id, params)
        self.assert_returns(shared_workflow.find, result)
        self.assert_typed(result)

    def test_find_run(self):
        run_id = 12345
        id = 12345
        params = {
            "id": 12345,
            "run_id": 12345,
        }
        result = shared_workflow.find_run(id, run_id, params)
        self.assert_returns(shared_workflow.find_run, result)
        self.assert_typed(result)

    def test_run_workflow(self):
        id = 12345
        params = {
            "id": 12345,
            "submission_revision": "foo",
            "submission_id": "foo",
            "file_path": "foo",
        }
        result = shared_workflow.run_workflow(id, params)
        self.assert_returns(shared_workflow.run_workflow, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

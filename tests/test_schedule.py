import unittest
from tests.base import TestBase
from files_sdk.models import Schedule
from files_sdk import schedule


class ScheduleTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        schedule = Schedule(params)
        result = schedule.update(params)
        self.assert_returns(Schedule.update, result)
        self.assert_typed(schedule)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        schedule = Schedule(params)
        schedule.delete(params)
        self.assert_typed(schedule)

    # Static Methods
    def test_list(self):
        result = schedule.list()
        self.assert_returns(schedule.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = schedule.find(id, params)
        self.assert_returns(schedule.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "name": "foo",
            "schedule_days_of_week": [1],
            "schedule_times_of_day": ["foo1"],
        }
        result = schedule.create(params)
        self.assert_returns(schedule.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = schedule.update(id, params)
        self.assert_returns(schedule.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = schedule.delete(id, params)
        self.assert_returns(schedule.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

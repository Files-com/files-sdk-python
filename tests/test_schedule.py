import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import Schedule
from files_sdk import schedule

class ScheduleTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/schedules/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        schedule = Schedule(params)
        schedule.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/schedules/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        schedule = Schedule(params)
        schedule.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/schedules"), "Mock path does not exist")
    def test_list(self):
        resp = schedule.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/schedules/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        schedule.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/schedules"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
            "schedule_days_of_week" : [1],
            "schedule_times_of_day" : ["foo1"],
        }
        schedule.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/schedules/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        schedule.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/schedules/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        schedule.delete(id, params)

if __name__ == '__main__':
    unittest.main()
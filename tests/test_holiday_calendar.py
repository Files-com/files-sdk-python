import unittest
import inspect
import files_sdk
from tests.base import TestBase
from files_sdk.models import HolidayCalendar
from files_sdk import holiday_calendar

class HolidayCalendarTest(TestBase):
    pass 
    # Instance Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/holiday_calendars/{id}"), "Mock path does not exist")
    def test_update(self):
        params = {
            "id" : 12345,
        }
        holiday_calendar = HolidayCalendar(params)
        holiday_calendar.update(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/holiday_calendars/{id}"), "Mock path does not exist")
    def test_delete(self):
        params = {
            "id" : 12345,
        }
        holiday_calendar = HolidayCalendar(params)
        holiday_calendar.delete(params)

    # Alias of delete
    def test_destroy(self):
        pass

    # Static Methods
    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/holiday_calendars"), "Mock path does not exist")
    def test_list(self):
        resp = holiday_calendar.list()

    @unittest.skipUnless(TestBase.mock_server_path_exists("GET", "/holiday_calendars/{id}"), "Mock path does not exist")
    def test_find(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        holiday_calendar.find(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("POST", "/holiday_calendars"), "Mock path does not exist")
    def test_create(self):
        params = {
            "name" : "foo",
        }
        holiday_calendar.create(params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("PATCH", "/holiday_calendars/{id}"), "Mock path does not exist")
    def test_update(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        holiday_calendar.update(id, params)

    @unittest.skipUnless(TestBase.mock_server_path_exists("DELETE", "/holiday_calendars/{id}"), "Mock path does not exist")
    def test_delete(self):
        id = 12345
        params = {
            "id" : 12345,
        }
        holiday_calendar.delete(id, params)

if __name__ == '__main__':
    unittest.main()
import unittest
from tests.base import TestBase
from files_sdk.models import HolidayCalendar
from files_sdk import holiday_calendar


class HolidayCalendarTest(TestBase):
    # Instance Methods
    def test_instance_update(self):
        params = {
            "id": 12345,
        }
        holiday_calendar = HolidayCalendar(params)
        result = holiday_calendar.update(params)
        self.assert_returns(HolidayCalendar.update, result)
        self.assert_typed(holiday_calendar)

    def test_instance_delete(self):
        params = {
            "id": 12345,
        }
        holiday_calendar = HolidayCalendar(params)
        holiday_calendar.delete(params)
        self.assert_typed(holiday_calendar)

    # Static Methods
    def test_list(self):
        result = holiday_calendar.list()
        self.assert_returns(holiday_calendar.list, result)
        self.assert_typed(result)

    def test_find(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = holiday_calendar.find(id, params)
        self.assert_returns(holiday_calendar.find, result)
        self.assert_typed(result)

    def test_create(self):
        params = {
            "definition": {},
            "name": "foo",
        }
        result = holiday_calendar.create(params)
        self.assert_returns(holiday_calendar.create, result)
        self.assert_typed(result)

    def test_update(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = holiday_calendar.update(id, params)
        self.assert_returns(holiday_calendar.update, result)
        self.assert_typed(result)

    def test_delete(self):
        id = 12345
        params = {
            "id": 12345,
        }
        result = holiday_calendar.delete(id, params)
        self.assert_returns(holiday_calendar.delete, result)
        self.assert_typed(result)


if __name__ == "__main__":
    unittest.main()

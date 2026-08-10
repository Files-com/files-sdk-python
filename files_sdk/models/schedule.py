import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Schedule:
    default_attributes = {
        "id": None,  # int64 - Schedule ID.
        "name": None,  # string - Schedule name.
        "schedule_days_of_week": None,  # array(int64) - 0-based weekdays used by the Schedule. 0 is Sunday.
        "schedule_times_of_day": None,  # array(string) - Times of day in HH:MM format (24-hour).
        "schedule_time_zone": None,  # string - Time zone for scheduled times. If not set, times are interpreted as UTC.
        "holiday_region": None,  # string - Optional holiday region on which linked resources do not run.
        "human_readable_schedule": None,  # string - Human-readable Schedule description.
        "created_at": None,  # date-time - Creation time.
        "updated_at": None,  # date-time - Last update time.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Schedule.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Schedule.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Parameters:
    #   name - string - Schedule name.
    #   schedule_days_of_week - array(int64) - 0-based weekdays used by the Schedule. 0 is Sunday.
    #   schedule_times_of_day - array(string) - Times of day in HH:MM format (24-hour).
    #   schedule_time_zone - string - Time zone for scheduled times. If not set, times are interpreted as UTC.
    #   holiday_region - string - Optional holiday region on which linked resources do not run.
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "schedule_days_of_week" in params and not isinstance(
            params["schedule_days_of_week"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_days_of_week must be an list"
            )
        if "schedule_times_of_day" in params and not isinstance(
            params["schedule_times_of_day"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_times_of_day must be an list"
            )
        if "schedule_time_zone" in params and not isinstance(
            params["schedule_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_time_zone must be an str"
            )
        if "holiday_region" in params and not isinstance(
            params["holiday_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: holiday_region must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/schedules/{id}".format(id=quote(str(params["id"]), safe="")),
            params,
            self.options,
        )
        return response.data

    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "DELETE",
            "/schedules/{id}".format(id=quote(str(params["id"]), safe="")),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            new_obj = self.update(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            return True
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    return ListObj(Schedule, "GET", "/schedules", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Schedule ID.
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET",
        "/schedules/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return Schedule(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name (required) - string - Schedule name.
#   schedule_days_of_week (required) - array(int64) - 0-based weekdays used by the Schedule. 0 is Sunday.
#   schedule_times_of_day (required) - array(string) - Times of day in HH:MM format (24-hour).
#   schedule_time_zone - string - Time zone for scheduled times. If not set, times are interpreted as UTC.
#   holiday_region - string - Optional holiday region on which linked resources do not run.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "schedule_days_of_week" in params and not isinstance(
        params["schedule_days_of_week"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_days_of_week must be an list"
        )
    if "schedule_times_of_day" in params and not isinstance(
        params["schedule_times_of_day"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_times_of_day must be an list"
        )
    if "schedule_time_zone" in params and not isinstance(
        params["schedule_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_time_zone must be an str"
        )
    if "holiday_region" in params and not isinstance(
        params["holiday_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: holiday_region must be an str"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    if "schedule_days_of_week" not in params:
        raise MissingParameterError("Parameter missing: schedule_days_of_week")
    if "schedule_times_of_day" not in params:
        raise MissingParameterError("Parameter missing: schedule_times_of_day")
    response, options = Api.send_request("POST", "/schedules", params, options)
    return Schedule(response.data, options)


# Parameters:
#   name - string - Schedule name.
#   schedule_days_of_week - array(int64) - 0-based weekdays used by the Schedule. 0 is Sunday.
#   schedule_times_of_day - array(string) - Times of day in HH:MM format (24-hour).
#   schedule_time_zone - string - Time zone for scheduled times. If not set, times are interpreted as UTC.
#   holiday_region - string - Optional holiday region on which linked resources do not run.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "schedule_days_of_week" in params and not isinstance(
        params["schedule_days_of_week"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_days_of_week must be an list"
        )
    if "schedule_times_of_day" in params and not isinstance(
        params["schedule_times_of_day"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_times_of_day must be an list"
        )
    if "schedule_time_zone" in params and not isinstance(
        params["schedule_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_time_zone must be an str"
        )
    if "holiday_region" in params and not isinstance(
        params["holiday_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: holiday_region must be an str"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/schedules/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return Schedule(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "DELETE",
        "/schedules/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Schedule(*args, **kwargs)

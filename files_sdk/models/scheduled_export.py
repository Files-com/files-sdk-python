import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ScheduledExport:
    default_attributes = {
        "id": None,  # int64 - Scheduled Export ID
        "name": None,  # string - Name for this scheduled export.
        "export_type": None,  # string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
        "report_name": None,  # string - Human-readable report name.
        "export_options": None,  # object - Report-specific options. `permission_audit` supports `group_by` with `user` or `path`.
        "user_id": None,  # int64 - Site Admin user who receives the completed export e-mail.
        "disabled": None,  # boolean - If true, this scheduled export will not run.
        "trigger": None,  # string - Schedule trigger type: `daily` or `custom_schedule`.
        "interval": None,  # string - If trigger is `daily`, this specifies how often to run the scheduled export.
        "recurring_day": None,  # int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        "schedule_times_of_day": None,  # array(string) - Times of day in HH:MM format for schedule-driven exports.
        "schedule_time_zone": None,  # string - Time zone used by the scheduled export.
        "holiday_region": None,  # string - Optional holiday region used by schedule-driven exports.
        "human_readable_schedule": None,  # string - Human-readable schedule description.
        "last_run_at": None,  # date-time - Most recent scheduled run time.
        "last_export_id": None,  # int64 - Most recent Export ID created by this schedule.
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
        for (
            attribute,
            default_value,
        ) in ScheduledExport.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ScheduledExport.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Parameters:
    #   name - string - Name for this scheduled export.
    #   export_type - string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
    #   export_options - object - Report-specific options. `permission_audit` supports `group_by` with `user` or `path`.
    #   user_id - int64 - Site Admin user who receives the completed export e-mail.
    #   disabled - boolean - If true, this scheduled export will not run.
    #   trigger - string - Schedule trigger type: `daily` or `custom_schedule`.
    #   interval - string - If trigger is `daily`, this specifies how often to run the scheduled export.
    #   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    #   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    #   schedule_times_of_day - array(string) - Times of day in HH:MM format for schedule-driven exports.
    #   schedule_time_zone - string - Time zone used by the scheduled export.
    #   holiday_region - string - Optional holiday region used by schedule-driven exports.
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
        if "export_type" in params and not isinstance(
            params["export_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: export_type must be an str"
            )
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "recurring_day" in params and not isinstance(
            params["recurring_day"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_day must be an int"
            )
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
            "/scheduled_exports/{id}".format(
                id=quote(str(params["id"]), safe="")
            ),
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
            "/scheduled_exports/{id}".format(
                id=quote(str(params["id"]), safe="")
            ),
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
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `export_type` or `disabled`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `export_type`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `export_type`.
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
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    return ListObj(
        ScheduledExport, "GET", "/scheduled_exports", params, options
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Scheduled Export ID.
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
        "/scheduled_exports/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return ScheduledExport(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name (required) - string - Name for this scheduled export.
#   export_type (required) - string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
#   export_options - object - Report-specific options. `permission_audit` supports `group_by` with `user` or `path`.
#   user_id - int64 - Site Admin user who receives the completed export e-mail.
#   disabled - boolean - If true, this scheduled export will not run.
#   trigger - string - Schedule trigger type: `daily` or `custom_schedule`.
#   interval - string - If trigger is `daily`, this specifies how often to run the scheduled export.
#   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
#   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
#   schedule_times_of_day - array(string) - Times of day in HH:MM format for schedule-driven exports.
#   schedule_time_zone - string - Time zone used by the scheduled export.
#   holiday_region - string - Optional holiday region used by schedule-driven exports.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "export_type" in params and not isinstance(params["export_type"], str):
        raise InvalidParameterError(
            "Bad parameter: export_type must be an str"
        )
    if "export_options" in params and not isinstance(
        params["export_options"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: export_options must be an dict"
        )
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "disabled" in params and not isinstance(params["disabled"], bool):
        raise InvalidParameterError("Bad parameter: disabled must be an bool")
    if "trigger" in params and not isinstance(params["trigger"], str):
        raise InvalidParameterError("Bad parameter: trigger must be an str")
    if "interval" in params and not isinstance(params["interval"], str):
        raise InvalidParameterError("Bad parameter: interval must be an str")
    if "recurring_day" in params and not isinstance(
        params["recurring_day"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: recurring_day must be an int"
        )
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
    if "export_type" not in params:
        raise MissingParameterError("Parameter missing: export_type")
    response, options = Api.send_request(
        "POST", "/scheduled_exports", params, options
    )
    return ScheduledExport(response.data, options)


# Parameters:
#   name - string - Name for this scheduled export.
#   export_type - string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
#   export_options - object - Report-specific options. `permission_audit` supports `group_by` with `user` or `path`.
#   user_id - int64 - Site Admin user who receives the completed export e-mail.
#   disabled - boolean - If true, this scheduled export will not run.
#   trigger - string - Schedule trigger type: `daily` or `custom_schedule`.
#   interval - string - If trigger is `daily`, this specifies how often to run the scheduled export.
#   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
#   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
#   schedule_times_of_day - array(string) - Times of day in HH:MM format for schedule-driven exports.
#   schedule_time_zone - string - Time zone used by the scheduled export.
#   holiday_region - string - Optional holiday region used by schedule-driven exports.
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
    if "export_type" in params and not isinstance(params["export_type"], str):
        raise InvalidParameterError(
            "Bad parameter: export_type must be an str"
        )
    if "export_options" in params and not isinstance(
        params["export_options"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: export_options must be an dict"
        )
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "disabled" in params and not isinstance(params["disabled"], bool):
        raise InvalidParameterError("Bad parameter: disabled must be an bool")
    if "trigger" in params and not isinstance(params["trigger"], str):
        raise InvalidParameterError("Bad parameter: trigger must be an str")
    if "interval" in params and not isinstance(params["interval"], str):
        raise InvalidParameterError("Bad parameter: interval must be an str")
    if "recurring_day" in params and not isinstance(
        params["recurring_day"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: recurring_day must be an int"
        )
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
        "/scheduled_exports/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return ScheduledExport(response.data, options)


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
        "/scheduled_exports/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return ScheduledExport(*args, **kwargs)

import builtins  # noqa: F401
from files_sdk.models.expectation_evaluation import ExpectationEvaluation
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Expectation:
    default_attributes = {
        "id": None,  # int64 - Expectation ID
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
        "name": None,  # string - Expectation name.
        "description": None,  # string - Expectation description.
        "path": None,  # string - Path scope for the expectation. Supports workspace-relative presentation. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "source": None,  # string - Source glob used to select candidate files.
        "exclude_pattern": None,  # string - Optional source exclusion glob.
        "disabled": None,  # boolean - If true, the expectation is disabled.
        "expectations_version": None,  # int64 - Criteria schema version for this expectation.
        "trigger": None,  # string - How this expectation opens windows.
        "interval": None,  # string - If trigger is `daily`, this specifies how often to run the expectation.
        "recurring_day": None,  # int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        "schedule_times_of_day": None,  # array(string) - Times of day in HH:MM format for schedule-driven expectations.
        "schedule_time_zone": None,  # string - Time zone used by the expectation schedule.
        "holiday_region": None,  # string - Optional holiday region used by schedule-driven expectations.
        "lookback_interval": None,  # int64 - How many seconds before the due boundary the window starts.
        "late_acceptance_interval": None,  # int64 - How many seconds a schedule-driven window may remain eligible to close as late.
        "inactivity_interval": None,  # int64 - How many quiet seconds are required before final closure.
        "max_open_interval": None,  # int64 - Hard-stop duration in seconds for unscheduled expectations.
        "criteria": None,  # object - Structured criteria v1 definition for the expectation.
        "last_evaluated_at": None,  # date-time - Last time this expectation was evaluated.
        "last_success_at": None,  # date-time - Last time this expectation closed successfully.
        "last_failure_at": None,  # date-time - Last time this expectation closed with a failure result.
        "last_result": None,  # string - Most recent terminal result for this expectation.
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
        for attribute, default_value in Expectation.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Expectation.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Manually open an Expectation window
    def trigger_evaluation(self, params=None):
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
        response, _options = Api.send_request(
            "POST",
            "/expectations/{id}/trigger_evaluation".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    # Parameters:
    #   name - string - Expectation name.
    #   description - string - Expectation description.
    #   path - string - Path scope for the expectation. Supports workspace-relative presentation.
    #   source - string - Source glob used to select candidate files.
    #   exclude_pattern - string - Optional source exclusion glob.
    #   disabled - boolean - If true, the expectation is disabled.
    #   trigger - string - How this expectation opens windows.
    #   interval - string - If trigger is `daily`, this specifies how often to run the expectation.
    #   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    #   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    #   schedule_times_of_day - array(string) - Times of day in HH:MM format for schedule-driven expectations.
    #   schedule_time_zone - string - Time zone used by the expectation schedule.
    #   holiday_region - string - Optional holiday region used by schedule-driven expectations.
    #   lookback_interval - int64 - How many seconds before the due boundary the window starts.
    #   late_acceptance_interval - int64 - How many seconds a schedule-driven window may remain eligible to close as late.
    #   inactivity_interval - int64 - How many quiet seconds are required before final closure.
    #   max_open_interval - int64 - Hard-stop duration in seconds for unscheduled expectations.
    #   criteria - object - Structured criteria v1 definition for the expectation.
    #   workspace_id - int64 - Workspace ID. `0` means the default workspace.
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
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "source" in params and not isinstance(params["source"], str):
            raise InvalidParameterError("Bad parameter: source must be an str")
        if "exclude_pattern" in params and not isinstance(
            params["exclude_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: exclude_pattern must be an str"
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
        if "lookback_interval" in params and not isinstance(
            params["lookback_interval"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: lookback_interval must be an int"
            )
        if "late_acceptance_interval" in params and not isinstance(
            params["late_acceptance_interval"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: late_acceptance_interval must be an int"
            )
        if "inactivity_interval" in params and not isinstance(
            params["inactivity_interval"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_interval must be an int"
            )
        if "max_open_interval" in params and not isinstance(
            params["max_open_interval"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: max_open_interval must be an int"
            )
        if "workspace_id" in params and not isinstance(
            params["workspace_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/expectations/{id}".format(id=params["id"]),
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
            "/expectations/{id}".format(id=params["id"]),
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
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name` or `disabled`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.
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
    return ListObj(Expectation, "GET", "/expectations", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Expectation ID.
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
        "GET", "/expectations/{id}".format(id=params["id"]), params, options
    )
    return Expectation(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name - string - Expectation name.
#   description - string - Expectation description.
#   path - string - Path scope for the expectation. Supports workspace-relative presentation.
#   source - string - Source glob used to select candidate files.
#   exclude_pattern - string - Optional source exclusion glob.
#   disabled - boolean - If true, the expectation is disabled.
#   trigger - string - How this expectation opens windows.
#   interval - string - If trigger is `daily`, this specifies how often to run the expectation.
#   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
#   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
#   schedule_times_of_day - array(string) - Times of day in HH:MM format for schedule-driven expectations.
#   schedule_time_zone - string - Time zone used by the expectation schedule.
#   holiday_region - string - Optional holiday region used by schedule-driven expectations.
#   lookback_interval - int64 - How many seconds before the due boundary the window starts.
#   late_acceptance_interval - int64 - How many seconds a schedule-driven window may remain eligible to close as late.
#   inactivity_interval - int64 - How many quiet seconds are required before final closure.
#   max_open_interval - int64 - Hard-stop duration in seconds for unscheduled expectations.
#   criteria - object - Structured criteria v1 definition for the expectation.
#   workspace_id - int64 - Workspace ID. `0` means the default workspace.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "source" in params and not isinstance(params["source"], str):
        raise InvalidParameterError("Bad parameter: source must be an str")
    if "exclude_pattern" in params and not isinstance(
        params["exclude_pattern"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: exclude_pattern must be an str"
        )
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
    if "lookback_interval" in params and not isinstance(
        params["lookback_interval"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: lookback_interval must be an int"
        )
    if "late_acceptance_interval" in params and not isinstance(
        params["late_acceptance_interval"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: late_acceptance_interval must be an int"
        )
    if "inactivity_interval" in params and not isinstance(
        params["inactivity_interval"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: inactivity_interval must be an int"
        )
    if "max_open_interval" in params and not isinstance(
        params["max_open_interval"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: max_open_interval must be an int"
        )
    if "criteria" in params and not isinstance(params["criteria"], dict):
        raise InvalidParameterError("Bad parameter: criteria must be an dict")
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: workspace_id must be an int"
        )
    response, options = Api.send_request(
        "POST", "/expectations", params, options
    )
    return Expectation(response.data, options)


# Manually open an Expectation window
def trigger_evaluation(id, params=None, options=None):
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
        "POST",
        "/expectations/{id}/trigger_evaluation".format(id=params["id"]),
        params,
        options,
    )
    return ExpectationEvaluation(response.data, options)


# Parameters:
#   name - string - Expectation name.
#   description - string - Expectation description.
#   path - string - Path scope for the expectation. Supports workspace-relative presentation.
#   source - string - Source glob used to select candidate files.
#   exclude_pattern - string - Optional source exclusion glob.
#   disabled - boolean - If true, the expectation is disabled.
#   trigger - string - How this expectation opens windows.
#   interval - string - If trigger is `daily`, this specifies how often to run the expectation.
#   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
#   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
#   schedule_times_of_day - array(string) - Times of day in HH:MM format for schedule-driven expectations.
#   schedule_time_zone - string - Time zone used by the expectation schedule.
#   holiday_region - string - Optional holiday region used by schedule-driven expectations.
#   lookback_interval - int64 - How many seconds before the due boundary the window starts.
#   late_acceptance_interval - int64 - How many seconds a schedule-driven window may remain eligible to close as late.
#   inactivity_interval - int64 - How many quiet seconds are required before final closure.
#   max_open_interval - int64 - Hard-stop duration in seconds for unscheduled expectations.
#   criteria - object - Structured criteria v1 definition for the expectation.
#   workspace_id - int64 - Workspace ID. `0` means the default workspace.
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
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "source" in params and not isinstance(params["source"], str):
        raise InvalidParameterError("Bad parameter: source must be an str")
    if "exclude_pattern" in params and not isinstance(
        params["exclude_pattern"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: exclude_pattern must be an str"
        )
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
    if "lookback_interval" in params and not isinstance(
        params["lookback_interval"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: lookback_interval must be an int"
        )
    if "late_acceptance_interval" in params and not isinstance(
        params["late_acceptance_interval"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: late_acceptance_interval must be an int"
        )
    if "inactivity_interval" in params and not isinstance(
        params["inactivity_interval"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: inactivity_interval must be an int"
        )
    if "max_open_interval" in params and not isinstance(
        params["max_open_interval"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: max_open_interval must be an int"
        )
    if "criteria" in params and not isinstance(params["criteria"], dict):
        raise InvalidParameterError("Bad parameter: criteria must be an dict")
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: workspace_id must be an int"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/expectations/{id}".format(id=params["id"]), params, options
    )
    return Expectation(response.data, options)


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
        "DELETE", "/expectations/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Expectation(*args, **kwargs)

import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AiTask:
    default_attributes = {
        "id": None,  # int64 - AI Task ID.
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
        "name": None,  # string - AI Task name.
        "description": None,  # string - AI Task description.
        "prompt": None,  # string - Prompt sent when this AI Task is invoked.
        "permission_set": None,  # string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
        "path": None,  # string - Path scope used for action-triggered AI Tasks. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "source": None,  # string - Source glob used with `path` for action-triggered AI Tasks.
        "disabled": None,  # boolean - If true, this AI Task will not run.
        "trigger": None,  # string - How this AI Task is triggered.
        "trigger_actions": None,  # array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
        "interval": None,  # string - If trigger is `daily`, this specifies how often to run the AI Task.
        "recurring_day": None,  # int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        "schedule_times_of_day": None,  # array(string) - Times of day in HH:MM format for scheduled AI Tasks.
        "schedule_time_zone": None,  # string - Time zone used by the AI Task schedule.
        "holiday_region": None,  # string - Optional holiday region used by scheduled AI Tasks.
        "human_readable_schedule": None,  # string - Human-readable schedule description.
        "last_run_at": None,  # date-time - Most recent successful invocation time.
        "master_admin_user_id": None,  # int64 - Master User ID used for AI Task invocations.
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
        for attribute, default_value in AiTask.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in AiTask.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    # Manually Run AI Task
    def manual_run(self, params=None):
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
            "POST",
            "/ai_tasks/{id}/manual_run".format(
                id=quote(str(params["id"]), safe="")
            ),
            params,
            self.options,
        )

    # Parameters:
    #   description - string - AI Task description.
    #   disabled - boolean - If true, this AI Task will not run.
    #   holiday_region - string - Optional holiday region used by scheduled AI Tasks.
    #   interval - string - If trigger is `daily`, this specifies how often to run the AI Task.
    #   name - string - AI Task name.
    #   path - string - Path scope used for action-triggered AI Tasks.
    #   permission_set - string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
    #   prompt - string - Prompt sent when this AI Task is invoked.
    #   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    #   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    #   schedule_time_zone - string - Time zone used by the AI Task schedule.
    #   schedule_times_of_day - array(string) - Times of day in HH:MM format for scheduled AI Tasks.
    #   source - string - Source glob used with `path` for action-triggered AI Tasks.
    #   trigger - string - How this AI Task is triggered.
    #   trigger_actions - array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
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
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "holiday_region" in params and not isinstance(
            params["holiday_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: holiday_region must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "permission_set" in params and not isinstance(
            params["permission_set"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: permission_set must be an str"
            )
        if "prompt" in params and not isinstance(params["prompt"], str):
            raise InvalidParameterError("Bad parameter: prompt must be an str")
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
        if "schedule_time_zone" in params and not isinstance(
            params["schedule_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_time_zone must be an str"
            )
        if "schedule_times_of_day" in params and not isinstance(
            params["schedule_times_of_day"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_times_of_day must be an list"
            )
        if "source" in params and not isinstance(params["source"], str):
            raise InvalidParameterError("Bad parameter: source must be an str")
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "trigger_actions" in params and not isinstance(
            params["trigger_actions"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: trigger_actions must be an list"
            )
        if "workspace_id" in params and not isinstance(
            params["workspace_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/ai_tasks/{id}".format(id=quote(str(params["id"]), safe="")),
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
            "/ai_tasks/{id}".format(id=quote(str(params["id"]), safe="")),
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
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `id`, `disabled` or `updated_at`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `trigger` or `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.
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
    return ListObj(AiTask, "GET", "/ai_tasks", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Ai Task ID.
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
        "/ai_tasks/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return AiTask(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   description - string - AI Task description.
#   disabled - boolean - If true, this AI Task will not run.
#   holiday_region - string - Optional holiday region used by scheduled AI Tasks.
#   interval - string - If trigger is `daily`, this specifies how often to run the AI Task.
#   name (required) - string - AI Task name.
#   path - string - Path scope used for action-triggered AI Tasks.
#   permission_set - string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
#   prompt (required) - string - Prompt sent when this AI Task is invoked.
#   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
#   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
#   schedule_time_zone - string - Time zone used by the AI Task schedule.
#   schedule_times_of_day - array(string) - Times of day in HH:MM format for scheduled AI Tasks.
#   source - string - Source glob used with `path` for action-triggered AI Tasks.
#   trigger - string - How this AI Task is triggered.
#   trigger_actions - array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
#   workspace_id - int64 - Workspace ID. `0` means the default workspace.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "disabled" in params and not isinstance(params["disabled"], bool):
        raise InvalidParameterError("Bad parameter: disabled must be an bool")
    if "holiday_region" in params and not isinstance(
        params["holiday_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: holiday_region must be an str"
        )
    if "interval" in params and not isinstance(params["interval"], str):
        raise InvalidParameterError("Bad parameter: interval must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "permission_set" in params and not isinstance(
        params["permission_set"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: permission_set must be an str"
        )
    if "prompt" in params and not isinstance(params["prompt"], str):
        raise InvalidParameterError("Bad parameter: prompt must be an str")
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
    if "schedule_time_zone" in params and not isinstance(
        params["schedule_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_time_zone must be an str"
        )
    if "schedule_times_of_day" in params and not isinstance(
        params["schedule_times_of_day"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_times_of_day must be an list"
        )
    if "source" in params and not isinstance(params["source"], str):
        raise InvalidParameterError("Bad parameter: source must be an str")
    if "trigger" in params and not isinstance(params["trigger"], str):
        raise InvalidParameterError("Bad parameter: trigger must be an str")
    if "trigger_actions" in params and not isinstance(
        params["trigger_actions"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: trigger_actions must be an list"
        )
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: workspace_id must be an int"
        )
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    if "prompt" not in params:
        raise MissingParameterError("Parameter missing: prompt")
    response, options = Api.send_request("POST", "/ai_tasks", params, options)
    return AiTask(response.data, options)


# Manually Run AI Task
def manual_run(id, params=None, options=None):
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
        "POST",
        "/ai_tasks/{id}/manual_run".format(
            id=quote(str(params["id"]), safe="")
        ),
        params,
        options,
    )


# Parameters:
#   description - string - AI Task description.
#   disabled - boolean - If true, this AI Task will not run.
#   holiday_region - string - Optional holiday region used by scheduled AI Tasks.
#   interval - string - If trigger is `daily`, this specifies how often to run the AI Task.
#   name - string - AI Task name.
#   path - string - Path scope used for action-triggered AI Tasks.
#   permission_set - string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
#   prompt - string - Prompt sent when this AI Task is invoked.
#   recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
#   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
#   schedule_time_zone - string - Time zone used by the AI Task schedule.
#   schedule_times_of_day - array(string) - Times of day in HH:MM format for scheduled AI Tasks.
#   source - string - Source glob used with `path` for action-triggered AI Tasks.
#   trigger - string - How this AI Task is triggered.
#   trigger_actions - array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
#   workspace_id - int64 - Workspace ID. `0` means the default workspace.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError(
            "Bad parameter: description must be an str"
        )
    if "disabled" in params and not isinstance(params["disabled"], bool):
        raise InvalidParameterError("Bad parameter: disabled must be an bool")
    if "holiday_region" in params and not isinstance(
        params["holiday_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: holiday_region must be an str"
        )
    if "interval" in params and not isinstance(params["interval"], str):
        raise InvalidParameterError("Bad parameter: interval must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "permission_set" in params and not isinstance(
        params["permission_set"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: permission_set must be an str"
        )
    if "prompt" in params and not isinstance(params["prompt"], str):
        raise InvalidParameterError("Bad parameter: prompt must be an str")
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
    if "schedule_time_zone" in params and not isinstance(
        params["schedule_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_time_zone must be an str"
        )
    if "schedule_times_of_day" in params and not isinstance(
        params["schedule_times_of_day"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_times_of_day must be an list"
        )
    if "source" in params and not isinstance(params["source"], str):
        raise InvalidParameterError("Bad parameter: source must be an str")
    if "trigger" in params and not isinstance(params["trigger"], str):
        raise InvalidParameterError("Bad parameter: trigger must be an str")
    if "trigger_actions" in params and not isinstance(
        params["trigger_actions"], builtins.list
    ):
        raise InvalidParameterError(
            "Bad parameter: trigger_actions must be an list"
        )
    if "workspace_id" in params and not isinstance(
        params["workspace_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: workspace_id must be an int"
        )
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/ai_tasks/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return AiTask(response.data, options)


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
        "/ai_tasks/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return AiTask(*args, **kwargs)

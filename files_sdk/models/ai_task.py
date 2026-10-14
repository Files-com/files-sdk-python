import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class AiTask:
    """A ai task record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - AI Task ID.
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
        name: string - AI Task name.
        description: string - AI Task description.
        prompt: string - Prompt sent when this AI Task is invoked.
        permission_set: string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
        path: string - Path scope used for action-triggered AI Tasks. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        source: string - Source glob used with `path` for action-triggered AI Tasks.
        disabled: boolean - If true, this AI Task will not run.
        trigger: string - How this AI Task is triggered.
        trigger_actions: array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
        interval: string - If trigger is `daily`, this specifies how often to run the AI Task.
        recurring_day: int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days: array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id: int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the AI Task's schedule fields.
        schedule_days_of_week: array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_times_of_day: array(string) - Times of day in HH:MM format for the AI Task schedule.
        schedule_time_zone: string - Time zone used by the AI Task schedule.
        holiday_region: string - Optional holiday region used by the AI Task schedule.
        human_readable_schedule: string - Human-readable schedule description.
        last_run_at: date-time - Most recent successful invocation time.
        master_admin_user_id: int64 - Master User ID used for AI Task invocations.
        created_at: date-time - Creation time.
        updated_at: date-time - Last update time.
    """

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
        "recurring_days": None,  # array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        "schedule_id": None,  # int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the AI Task's schedule fields.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        "schedule_times_of_day": None,  # array(string) - Times of day in HH:MM format for the AI Task schedule.
        "schedule_time_zone": None,  # string - Time zone used by the AI Task schedule.
        "holiday_region": None,  # string - Optional holiday region used by the AI Task schedule.
        "human_readable_schedule": None,  # string - Human-readable schedule description.
        "last_run_at": None,  # date-time - Most recent successful invocation time.
        "master_admin_user_id": None,  # int64 - Master User ID used for AI Task invocations.
        "created_at": None,  # date-time - Creation time.
        "updated_at": None,  # date-time - Last update time.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    name: str | None
    description: str | None
    prompt: str | None
    permission_set: str | None
    path: str | None
    source: str | None
    disabled: bool | None
    trigger: str | None
    trigger_actions: builtins.list[str] | None
    interval: str | None
    recurring_day: int | None
    recurring_days: builtins.list[int] | None
    schedule_id: int | None
    schedule_days_of_week: builtins.list[int] | None
    schedule_times_of_day: builtins.list[str] | None
    schedule_time_zone: str | None
    holiday_region: str | None
    human_readable_schedule: str | None
    last_run_at: str | None
    master_admin_user_id: int | None
    created_at: str | None
    updated_at: str | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

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

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def manual_run(self, params: dict[str, Any] | None = None) -> None:
        """Manually Run AI Task"""
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "POST",
            "/ai_tasks/" + path_value(params["id"]) + "/manual_run",
            params,
        )

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          description - string - AI Task description.
          disabled - boolean - If true, this AI Task will not run.
          holiday_region - string - Optional holiday region used by the AI Task schedule.
          interval - string - If trigger is `daily`, this specifies how often to run the AI Task.
          name - string - AI Task name.
          path - string - Path scope used for action-triggered AI Tasks.
          permission_set - string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
          prompt - string - Prompt sent when this AI Task is invoked.
          recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
          recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
          schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the AI Task's schedule fields.
          schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
          schedule_time_zone - string - Time zone used by the AI Task schedule.
          schedule_times_of_day - array(string) - Times of day in HH:MM format for the AI Task schedule.
          source - string - Source glob used with `path` for action-triggered AI Tasks.
          trigger - string - How this AI Task is triggered.
          trigger_actions - array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
          workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "disabled" in params and isinstance(
            params["disabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
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
        if "recurring_day" in params and (
            not isinstance(params["recurring_day"], int)
            or isinstance(params["recurring_day"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_day must be an int"
            )
        if "recurring_days" in params and not isinstance(
            params["recurring_days"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_days must be an list"
            )
        if "schedule_id" in params and (
            not isinstance(params["schedule_id"], int)
            or isinstance(params["schedule_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_id must be an int"
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
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/ai_tasks/" + path_value(params["id"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/ai_tasks/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = AiTaskResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class AiTaskResource:
    """AiTask operations that use one client's configuration.

    Get one from a client, such as ``client.ai_task``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[AiTask]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name`, `disabled` or `updated_at`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `trigger` or `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(AiTask, "GET", "/ai_tasks", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[AiTask]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AiTask:
        """Parameters:
        id (required) - int64 - Ai Task ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> AiTask:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/ai_tasks/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, AiTask)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AiTask:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AiTask:
        """Parameters:
        description - string - AI Task description.
        disabled - boolean - If true, this AI Task will not run.
        holiday_region - string - Optional holiday region used by the AI Task schedule.
        interval - string - If trigger is `daily`, this specifies how often to run the AI Task.
        name (required) - string - AI Task name.
        path - string - Path scope used for action-triggered AI Tasks.
        permission_set - string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
        prompt (required) - string - Prompt sent when this AI Task is invoked.
        recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the AI Task's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_time_zone - string - Time zone used by the AI Task schedule.
        schedule_times_of_day - array(string) - Times of day in HH:MM format for the AI Task schedule.
        source - string - Source glob used with `path` for action-triggered AI Tasks.
        trigger - string - How this AI Task is triggered.
        trigger_actions - array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        params = copy_params(params)
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
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
        if "recurring_day" in params and (
            not isinstance(params["recurring_day"], int)
            or isinstance(params["recurring_day"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_day must be an int"
            )
        if "recurring_days" in params and not isinstance(
            params["recurring_days"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_days must be an list"
            )
        if "schedule_id" in params and (
            not isinstance(params["schedule_id"], int)
            or isinstance(params["schedule_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_id must be an int"
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
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        if "prompt" not in params:
            raise MissingParameterError("Parameter missing: prompt")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/ai_tasks", params)
        return operation.decode_model(response, AiTask)

    def manual_run(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Manually Run AI Task"""
        return self.__manual_run({"id": id}, params, options)

    def __manual_run(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST",
            "/ai_tasks/" + path_value(params["id"]) + "/manual_run",
            params,
        )

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AiTask:
        """Parameters:
        description - string - AI Task description.
        disabled - boolean - If true, this AI Task will not run.
        holiday_region - string - Optional holiday region used by the AI Task schedule.
        interval - string - If trigger is `daily`, this specifies how often to run the AI Task.
        name - string - AI Task name.
        path - string - Path scope used for action-triggered AI Tasks.
        permission_set - string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
        prompt - string - Prompt sent when this AI Task is invoked.
        recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the AI Task's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_time_zone - string - Time zone used by the AI Task schedule.
        schedule_times_of_day - array(string) - Times of day in HH:MM format for the AI Task schedule.
        source - string - Source glob used with `path` for action-triggered AI Tasks.
        trigger - string - How this AI Task is triggered.
        trigger_actions - array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> AiTask:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
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
        if "recurring_day" in params and (
            not isinstance(params["recurring_day"], int)
            or isinstance(params["recurring_day"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_day must be an int"
            )
        if "recurring_days" in params and not isinstance(
            params["recurring_days"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_days must be an list"
            )
        if "schedule_id" in params and (
            not isinstance(params["schedule_id"], int)
            or isinstance(params["schedule_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_id must be an int"
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
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/ai_tasks/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, AiTask)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/ai_tasks/" + path_value(params["id"]), params
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AiTask:
        """A new AiTask with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = AiTask(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = AiTaskResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[AiTask]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name`, `disabled` or `updated_at`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `trigger` or `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[AiTask]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AiTask:
    """Parameters:
    id (required) - int64 - Ai Task ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AiTask:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AiTask:
    """Parameters:
    description - string - AI Task description.
    disabled - boolean - If true, this AI Task will not run.
    holiday_region - string - Optional holiday region used by the AI Task schedule.
    interval - string - If trigger is `daily`, this specifies how often to run the AI Task.
    name (required) - string - AI Task name.
    path - string - Path scope used for action-triggered AI Tasks.
    permission_set - string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
    prompt (required) - string - Prompt sent when this AI Task is invoked.
    recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the AI Task's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    schedule_time_zone - string - Time zone used by the AI Task schedule.
    schedule_times_of_day - array(string) - Times of day in HH:MM format for the AI Task schedule.
    source - string - Source glob used with `path` for action-triggered AI Tasks.
    trigger - string - How this AI Task is triggered.
    trigger_actions - array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
    """
    return _legacy_resource.create(params, options)


def manual_run(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Manually Run AI Task"""
    _legacy_resource.manual_run(id, params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AiTask:
    """Parameters:
    description - string - AI Task description.
    disabled - boolean - If true, this AI Task will not run.
    holiday_region - string - Optional holiday region used by the AI Task schedule.
    interval - string - If trigger is `daily`, this specifies how often to run the AI Task.
    name - string - AI Task name.
    path - string - Path scope used for action-triggered AI Tasks.
    permission_set - string - Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
    prompt - string - Prompt sent when this AI Task is invoked.
    recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the AI Task's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    schedule_time_zone - string - Time zone used by the AI Task schedule.
    schedule_times_of_day - array(string) - Times of day in HH:MM format for the AI Task schedule.
    source - string - Source glob used with `path` for action-triggered AI Tasks.
    trigger - string - How this AI Task is triggered.
    trigger_actions - array(string) - If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> AiTask:
    return AiTask(*args, **kwargs)

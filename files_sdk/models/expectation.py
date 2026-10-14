import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.models.expectation_evaluation import ExpectationEvaluation
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


class Expectation:
    """A expectation record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Expectation ID
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
        name: string - Expectation name.
        description: string - Expectation description.
        path: string - Path scope for the expectation. Supports workspace-relative presentation. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        source: string - Source glob used to select candidate files.
        exclude_pattern: string - Optional source exclusion glob.
        disabled: boolean - If true, the expectation is disabled.
        expectations_version: int64 - Criteria schema version for this expectation.
        trigger: string - How this expectation opens windows.
        interval: string - If trigger is `daily`, this specifies how often to run the expectation.
        recurring_day: int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days: array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id: int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the Expectation's schedule fields.
        schedule_days_of_week: array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_times_of_day: array(string) - Times of day in HH:MM format for the Expectation schedule.
        schedule_time_zone: string - Time zone used by the Expectation schedule.
        holiday_region: string - Optional holiday region used by the Expectation schedule.
        lookback_interval: int64 - How many seconds before the due boundary the window starts.
        late_acceptance_interval: int64 - How many seconds a schedule-driven window may remain eligible to close as late.
        inactivity_interval: int64 - How many quiet seconds are required before final closure.
        max_open_interval: int64 - Hard-stop duration in seconds for unscheduled expectations.
        criteria: object - Versioned success criteria definition for the expectation. Criteria v2 supports optional FTS content validation.
        last_evaluated_at: date-time - Last time this expectation was evaluated.
        last_success_at: date-time - Last time this expectation closed successfully.
        last_failure_at: date-time - Last time this expectation closed with a failure result.
        last_result: string - Most recent terminal result for this expectation.
        created_at: date-time - Creation time.
        updated_at: date-time - Last update time.
    """

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
        "recurring_days": None,  # array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        "schedule_id": None,  # int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the Expectation's schedule fields.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        "schedule_times_of_day": None,  # array(string) - Times of day in HH:MM format for the Expectation schedule.
        "schedule_time_zone": None,  # string - Time zone used by the Expectation schedule.
        "holiday_region": None,  # string - Optional holiday region used by the Expectation schedule.
        "lookback_interval": None,  # int64 - How many seconds before the due boundary the window starts.
        "late_acceptance_interval": None,  # int64 - How many seconds a schedule-driven window may remain eligible to close as late.
        "inactivity_interval": None,  # int64 - How many quiet seconds are required before final closure.
        "max_open_interval": None,  # int64 - Hard-stop duration in seconds for unscheduled expectations.
        "criteria": None,  # object - Versioned success criteria definition for the expectation. Criteria v2 supports optional FTS content validation.
        "last_evaluated_at": None,  # date-time - Last time this expectation was evaluated.
        "last_success_at": None,  # date-time - Last time this expectation closed successfully.
        "last_failure_at": None,  # date-time - Last time this expectation closed with a failure result.
        "last_result": None,  # string - Most recent terminal result for this expectation.
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
    path: str | None
    source: str | None
    exclude_pattern: str | None
    disabled: bool | None
    expectations_version: int | None
    trigger: str | None
    interval: str | None
    recurring_day: int | None
    recurring_days: builtins.list[int] | None
    schedule_id: int | None
    schedule_days_of_week: builtins.list[int] | None
    schedule_times_of_day: builtins.list[str] | None
    schedule_time_zone: str | None
    holiday_region: str | None
    lookback_interval: int | None
    late_acceptance_interval: int | None
    inactivity_interval: int | None
    max_open_interval: int | None
    criteria: dict[str, Any] | None
    last_evaluated_at: str | None
    last_success_at: str | None
    last_failure_at: str | None
    last_result: str | None
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

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def trigger_evaluation(
        self, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Manually open an Expectation window"""
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
        response = operation.request(
            "POST",
            "/expectations/"
            + path_value(params["id"])
            + "/trigger_evaluation",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          name - string - Expectation name.
          description - string - Expectation description.
          path - string - Path scope for the expectation. Supports workspace-relative presentation.
          source - string - Source glob used to select candidate files.
          exclude_pattern - string - Optional source exclusion glob.
          disabled - boolean - If true, the expectation is disabled.
          trigger - string - How this expectation opens windows.
          interval - string - If trigger is `daily`, this specifies how often to run the expectation.
          recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
          recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
          schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the Expectation's schedule fields.
          schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
          schedule_times_of_day - array(string) - Times of day in HH:MM format for the Expectation schedule.
          schedule_time_zone - string - Time zone used by the Expectation schedule.
          holiday_region - string - Optional holiday region used by the Expectation schedule.
          lookback_interval - int64 - How many seconds before the due boundary the window starts.
          late_acceptance_interval - int64 - How many seconds a schedule-driven window may remain eligible to close as late.
          inactivity_interval - int64 - How many quiet seconds are required before final closure.
          max_open_interval - int64 - Hard-stop duration in seconds for unscheduled expectations.
          criteria - object - Versioned success criteria definition for the expectation, including optional Files Transform Script content validation in criteria v2.
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
        if "disabled" in params and isinstance(
            params["disabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
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
        if "lookback_interval" in params and (
            not isinstance(params["lookback_interval"], int)
            or isinstance(params["lookback_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: lookback_interval must be an int"
            )
        if "late_acceptance_interval" in params and (
            not isinstance(params["late_acceptance_interval"], int)
            or isinstance(params["late_acceptance_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: late_acceptance_interval must be an int"
            )
        if "inactivity_interval" in params and (
            not isinstance(params["inactivity_interval"], int)
            or isinstance(params["inactivity_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_interval must be an int"
            )
        if "max_open_interval" in params and (
            not isinstance(params["max_open_interval"], int)
            or isinstance(params["max_open_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: max_open_interval must be an int"
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
            "PATCH", "/expectations/" + path_value(params["id"]), params
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
            "DELETE", "/expectations/" + path_value(params["id"]), params
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
            new_obj = ExpectationResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class ExpectationResource:
    """Expectation operations that use one client's configuration.

    Get one from a client, such as ``client.expectation``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Expectation]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name` or `disabled`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.
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
        return ListObj(Expectation, "GET", "/expectations", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Expectation]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Expectation:
        """Parameters:
        id (required) - int64 - Expectation ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Expectation:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/expectations/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Expectation)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Expectation:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Expectation:
        """Parameters:
        name - string - Expectation name.
        description - string - Expectation description.
        path - string - Path scope for the expectation. Supports workspace-relative presentation.
        source - string - Source glob used to select candidate files.
        exclude_pattern - string - Optional source exclusion glob.
        disabled - boolean - If true, the expectation is disabled.
        trigger - string - How this expectation opens windows.
        interval - string - If trigger is `daily`, this specifies how often to run the expectation.
        recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the Expectation's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_times_of_day - array(string) - Times of day in HH:MM format for the Expectation schedule.
        schedule_time_zone - string - Time zone used by the Expectation schedule.
        holiday_region - string - Optional holiday region used by the Expectation schedule.
        lookback_interval - int64 - How many seconds before the due boundary the window starts.
        late_acceptance_interval - int64 - How many seconds a schedule-driven window may remain eligible to close as late.
        inactivity_interval - int64 - How many quiet seconds are required before final closure.
        max_open_interval - int64 - Hard-stop duration in seconds for unscheduled expectations.
        criteria - object - Versioned success criteria definition for the expectation, including optional Files Transform Script content validation in criteria v2.
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        params = copy_params(params)
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
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
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
        if "lookback_interval" in params and (
            not isinstance(params["lookback_interval"], int)
            or isinstance(params["lookback_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: lookback_interval must be an int"
            )
        if "late_acceptance_interval" in params and (
            not isinstance(params["late_acceptance_interval"], int)
            or isinstance(params["late_acceptance_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: late_acceptance_interval must be an int"
            )
        if "inactivity_interval" in params and (
            not isinstance(params["inactivity_interval"], int)
            or isinstance(params["inactivity_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_interval must be an int"
            )
        if "max_open_interval" in params and (
            not isinstance(params["max_open_interval"], int)
            or isinstance(params["max_open_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: max_open_interval must be an int"
            )
        if "criteria" in params and not isinstance(params["criteria"], dict):
            raise InvalidParameterError(
                "Bad parameter: criteria must be an dict"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/expectations", params)
        return operation.decode_model(response, Expectation)

    def trigger_evaluation(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ExpectationEvaluation:
        """Manually open an Expectation window"""
        return self.__trigger_evaluation({"id": id}, params, options)

    def __trigger_evaluation(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ExpectationEvaluation:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "POST",
            "/expectations/"
            + path_value(params["id"])
            + "/trigger_evaluation",
            params,
        )
        return operation.decode_model(response, ExpectationEvaluation)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Expectation:
        """Parameters:
        name - string - Expectation name.
        description - string - Expectation description.
        path - string - Path scope for the expectation. Supports workspace-relative presentation.
        source - string - Source glob used to select candidate files.
        exclude_pattern - string - Optional source exclusion glob.
        disabled - boolean - If true, the expectation is disabled.
        trigger - string - How this expectation opens windows.
        interval - string - If trigger is `daily`, this specifies how often to run the expectation.
        recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the Expectation's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_times_of_day - array(string) - Times of day in HH:MM format for the Expectation schedule.
        schedule_time_zone - string - Time zone used by the Expectation schedule.
        holiday_region - string - Optional holiday region used by the Expectation schedule.
        lookback_interval - int64 - How many seconds before the due boundary the window starts.
        late_acceptance_interval - int64 - How many seconds a schedule-driven window may remain eligible to close as late.
        inactivity_interval - int64 - How many quiet seconds are required before final closure.
        max_open_interval - int64 - Hard-stop duration in seconds for unscheduled expectations.
        criteria - object - Versioned success criteria definition for the expectation, including optional Files Transform Script content validation in criteria v2.
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Expectation:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
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
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
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
        if "lookback_interval" in params and (
            not isinstance(params["lookback_interval"], int)
            or isinstance(params["lookback_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: lookback_interval must be an int"
            )
        if "late_acceptance_interval" in params and (
            not isinstance(params["late_acceptance_interval"], int)
            or isinstance(params["late_acceptance_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: late_acceptance_interval must be an int"
            )
        if "inactivity_interval" in params and (
            not isinstance(params["inactivity_interval"], int)
            or isinstance(params["inactivity_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_interval must be an int"
            )
        if "max_open_interval" in params and (
            not isinstance(params["max_open_interval"], int)
            or isinstance(params["max_open_interval"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: max_open_interval must be an int"
            )
        if "criteria" in params and not isinstance(params["criteria"], dict):
            raise InvalidParameterError(
                "Bad parameter: criteria must be an dict"
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
            "PATCH", "/expectations/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Expectation)

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
            "DELETE", "/expectations/" + path_value(params["id"]), params
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
    ) -> Expectation:
        """A new Expectation with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Expectation(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ExpectationResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Expectation]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name` or `disabled`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Expectation]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Expectation:
    """Parameters:
    id (required) - int64 - Expectation ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Expectation:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Expectation:
    """Parameters:
    name - string - Expectation name.
    description - string - Expectation description.
    path - string - Path scope for the expectation. Supports workspace-relative presentation.
    source - string - Source glob used to select candidate files.
    exclude_pattern - string - Optional source exclusion glob.
    disabled - boolean - If true, the expectation is disabled.
    trigger - string - How this expectation opens windows.
    interval - string - If trigger is `daily`, this specifies how often to run the expectation.
    recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the Expectation's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    schedule_times_of_day - array(string) - Times of day in HH:MM format for the Expectation schedule.
    schedule_time_zone - string - Time zone used by the Expectation schedule.
    holiday_region - string - Optional holiday region used by the Expectation schedule.
    lookback_interval - int64 - How many seconds before the due boundary the window starts.
    late_acceptance_interval - int64 - How many seconds a schedule-driven window may remain eligible to close as late.
    inactivity_interval - int64 - How many quiet seconds are required before final closure.
    max_open_interval - int64 - Hard-stop duration in seconds for unscheduled expectations.
    criteria - object - Versioned success criteria definition for the expectation, including optional Files Transform Script content validation in criteria v2.
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
    """
    return _legacy_resource.create(params, options)


def trigger_evaluation(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ExpectationEvaluation:
    """Manually open an Expectation window"""
    return _legacy_resource.trigger_evaluation(id, params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Expectation:
    """Parameters:
    name - string - Expectation name.
    description - string - Expectation description.
    path - string - Path scope for the expectation. Supports workspace-relative presentation.
    source - string - Source glob used to select candidate files.
    exclude_pattern - string - Optional source exclusion glob.
    disabled - boolean - If true, the expectation is disabled.
    trigger - string - How this expectation opens windows.
    interval - string - If trigger is `daily`, this specifies how often to run the expectation.
    recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the Expectation's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    schedule_times_of_day - array(string) - Times of day in HH:MM format for the Expectation schedule.
    schedule_time_zone - string - Time zone used by the Expectation schedule.
    holiday_region - string - Optional holiday region used by the Expectation schedule.
    lookback_interval - int64 - How many seconds before the due boundary the window starts.
    late_acceptance_interval - int64 - How many seconds a schedule-driven window may remain eligible to close as late.
    inactivity_interval - int64 - How many quiet seconds are required before final closure.
    max_open_interval - int64 - Hard-stop duration in seconds for unscheduled expectations.
    criteria - object - Versioned success criteria definition for the expectation, including optional Files Transform Script content validation in criteria v2.
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


def new(*args, **kwargs) -> Expectation:
    return Expectation(*args, **kwargs)

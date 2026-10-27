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


class ScheduledExport:
    """A scheduled export record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Scheduled Export ID
        name: string - Name for this scheduled export.
        export_type: string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
        report_name: string - Human-readable report name.
        export_options: object - Options for the report selected by export_type.
        user_id: int64 - Site Admin user who receives the completed export e-mail.
        disabled: boolean - If true, this scheduled export will not run.
        trigger: string - Schedule trigger type: `daily` or `custom_schedule`.
        interval: string - If trigger is `daily`, this specifies how often to run the scheduled export.
        recurring_day: int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days: array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id: int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the scheduled export's schedule fields.
        schedule_days_of_week: array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_times_of_day: array(string) - Times of day in HH:MM format for the scheduled export schedule.
        schedule_time_zone: string - Time zone used by the scheduled export schedule.
        holiday_region: string - Optional holiday region used by the scheduled export schedule.
        human_readable_schedule: string - Human-readable schedule description.
        last_run_at: date-time - Most recent scheduled attempt time, including attempts that failed validation.
        last_export_id: int64 - Most recent Export ID created by this schedule.
        last_error: string - Validation error from the most recent scheduled attempt. The schedule remains enabled and retries at its next scheduled time. Cleared when an export is successfully created; does not describe errors during export generation.
        created_at: date-time - Creation time.
        updated_at: date-time - Last update time.
    """

    default_attributes = {
        "id": None,  # int64 - Scheduled Export ID
        "name": None,  # string - Name for this scheduled export.
        "export_type": None,  # string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
        "report_name": None,  # string - Human-readable report name.
        "export_options": None,  # object - Options for the report selected by export_type.
        "user_id": None,  # int64 - Site Admin user who receives the completed export e-mail.
        "disabled": None,  # boolean - If true, this scheduled export will not run.
        "trigger": None,  # string - Schedule trigger type: `daily` or `custom_schedule`.
        "interval": None,  # string - If trigger is `daily`, this specifies how often to run the scheduled export.
        "recurring_day": None,  # int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        "recurring_days": None,  # array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        "schedule_id": None,  # int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the scheduled export's schedule fields.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        "schedule_times_of_day": None,  # array(string) - Times of day in HH:MM format for the scheduled export schedule.
        "schedule_time_zone": None,  # string - Time zone used by the scheduled export schedule.
        "holiday_region": None,  # string - Optional holiday region used by the scheduled export schedule.
        "human_readable_schedule": None,  # string - Human-readable schedule description.
        "last_run_at": None,  # date-time - Most recent scheduled attempt time, including attempts that failed validation.
        "last_export_id": None,  # int64 - Most recent Export ID created by this schedule.
        "last_error": None,  # string - Validation error from the most recent scheduled attempt. The schedule remains enabled and retries at its next scheduled time. Cleared when an export is successfully created; does not describe errors during export generation.
        "created_at": None,  # date-time - Creation time.
        "updated_at": None,  # date-time - Last update time.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    export_type: str | None
    report_name: str | None
    export_options: dict[str, Any] | None
    user_id: int | None
    disabled: bool | None
    trigger: str | None
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
    last_export_id: int | None
    last_error: str | None
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

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          name - string - Name for this scheduled export.
          export_type - string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
          export_options - object - Options for the report selected by export_type.
          user_id - int64 - Site Admin user who receives the completed export e-mail.
          disabled - boolean - If true, this scheduled export will not run.
          trigger - string - Schedule trigger type: `daily` or `custom_schedule`.
          interval - string - If trigger is `daily`, this specifies how often to run the scheduled export.
          recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
          recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
          schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the scheduled export's schedule fields.
          schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
          schedule_times_of_day - array(string) - Times of day in HH:MM format for the scheduled export schedule.
          schedule_time_zone - string - Time zone used by the scheduled export schedule.
          holiday_region - string - Optional holiday region used by the scheduled export schedule.
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
        if "export_type" in params and not isinstance(
            params["export_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: export_type must be an str"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
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
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/scheduled_exports/" + path_value(params["id"]), params
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
            "DELETE", "/scheduled_exports/" + path_value(params["id"]), params
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
            new_obj = ScheduledExportResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class ScheduledExportResource:
    """ScheduledExport operations that use one client's configuration.

    Get one from a client, such as ``client.scheduled_export``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ScheduledExport]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `export_type` or `disabled`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `export_type`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `export_type`.
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
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            ScheduledExport, "GET", "/scheduled_exports", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ScheduledExport]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ScheduledExport:
        """Parameters:
        id (required) - int64 - Scheduled Export ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ScheduledExport:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/scheduled_exports/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, ScheduledExport)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ScheduledExport:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ScheduledExport:
        """Parameters:
        name (required) - string - Name for this scheduled export.
        export_type (required) - string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
        export_options - object - Options for the report selected by export_type.
        user_id - int64 - Site Admin user who receives the completed export e-mail.
        disabled - boolean - If true, this scheduled export will not run.
        trigger - string - Schedule trigger type: `daily` or `custom_schedule`.
        interval - string - If trigger is `daily`, this specifies how often to run the scheduled export.
        recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the scheduled export's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_times_of_day - array(string) - Times of day in HH:MM format for the scheduled export schedule.
        schedule_time_zone - string - Time zone used by the scheduled export schedule.
        holiday_region - string - Optional holiday region used by the scheduled export schedule.
        """
        params = copy_params(params)
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "export_type" in params and not isinstance(
            params["export_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: export_type must be an str"
            )
        if "export_options" in params and not isinstance(
            params["export_options"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: export_options must be an dict"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
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
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        if "export_type" not in params:
            raise MissingParameterError("Parameter missing: export_type")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/scheduled_exports", params)
        return operation.decode_model(response, ScheduledExport)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ScheduledExport:
        """Parameters:
        name - string - Name for this scheduled export.
        export_type - string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
        export_options - object - Options for the report selected by export_type.
        user_id - int64 - Site Admin user who receives the completed export e-mail.
        disabled - boolean - If true, this scheduled export will not run.
        trigger - string - Schedule trigger type: `daily` or `custom_schedule`.
        interval - string - If trigger is `daily`, this specifies how often to run the scheduled export.
        recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
        recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the scheduled export's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
        schedule_times_of_day - array(string) - Times of day in HH:MM format for the scheduled export schedule.
        schedule_time_zone - string - Time zone used by the scheduled export schedule.
        holiday_region - string - Optional holiday region used by the scheduled export schedule.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> ScheduledExport:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "export_type" in params and not isinstance(
            params["export_type"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: export_type must be an str"
            )
        if "export_options" in params and not isinstance(
            params["export_options"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: export_options must be an dict"
            )
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
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
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/scheduled_exports/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, ScheduledExport)

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
            "DELETE", "/scheduled_exports/" + path_value(params["id"]), params
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
    ) -> ScheduledExport:
        """A new ScheduledExport with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = ScheduledExport(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ScheduledExportResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ScheduledExport]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `export_type` or `disabled`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `export_type`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `export_type`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ScheduledExport]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ScheduledExport:
    """Parameters:
    id (required) - int64 - Scheduled Export ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ScheduledExport:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ScheduledExport:
    """Parameters:
    name (required) - string - Name for this scheduled export.
    export_type (required) - string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
    export_options - object - Options for the report selected by export_type.
    user_id - int64 - Site Admin user who receives the completed export e-mail.
    disabled - boolean - If true, this scheduled export will not run.
    trigger - string - Schedule trigger type: `daily` or `custom_schedule`.
    interval - string - If trigger is `daily`, this specifies how often to run the scheduled export.
    recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the scheduled export's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    schedule_times_of_day - array(string) - Times of day in HH:MM format for the scheduled export schedule.
    schedule_time_zone - string - Time zone used by the scheduled export schedule.
    holiday_region - string - Optional holiday region used by the scheduled export schedule.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ScheduledExport:
    """Parameters:
    name - string - Name for this scheduled export.
    export_type - string - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
    export_options - object - Options for the report selected by export_type.
    user_id - int64 - Site Admin user who receives the completed export e-mail.
    disabled - boolean - If true, this scheduled export will not run.
    trigger - string - Schedule trigger type: `daily` or `custom_schedule`.
    interval - string - If trigger is `daily`, this specifies how often to run the scheduled export.
    recurring_day - int64 - If trigger is `daily`, this selects the day number inside the chosen interval.
    recurring_days - array(int64) - If trigger is `daily`, this selects one or more day numbers inside a `week`, `month`, `quarter`, or `year` interval.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the scheduled export's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
    schedule_times_of_day - array(string) - Times of day in HH:MM format for the scheduled export schedule.
    schedule_time_zone - string - Time zone used by the scheduled export schedule.
    holiday_region - string - Optional holiday region used by the scheduled export schedule.
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


def new(*args, **kwargs) -> ScheduledExport:
    return ScheduledExport(*args, **kwargs)

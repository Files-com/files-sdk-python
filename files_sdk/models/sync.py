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


class Sync:
    """A sync record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Sync ID
        name: string - Name for this sync job
        description: string - Description for this sync job
        site_id: int64 - Site ID this sync belongs to
        workspace_id: int64 - Workspace ID this sync belongs to
        user_id: int64 - User who created or owns this sync
        src_path: string - Absolute source path for the sync
        dest_path: string - Absolute destination path for the sync
        src_remote_server_id: int64 - Remote server ID for the source (if remote)
        dest_remote_server_id: int64 - Remote server ID for the destination (if remote)
        src_site_id: int64 - Source site ID if syncing from a child or partner site
        dest_site_id: int64 - Destination site ID if syncing to a child or partner site
        two_way: boolean - Is this a two-way sync?
        keep_after_copy: boolean - Keep files after copying?
        delete_empty_folders: boolean - Delete empty folders after sync?
        disabled: boolean - Is this sync disabled?
        trigger: string - Trigger type: daily, custom_schedule, or manual
        trigger_file: string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
        always_write_trigger_file: boolean - If true, the trigger file will be sent at the end of a successful sync even when no files were transferred.
        include_patterns: array(string) - Array of glob patterns to include
        exclude_patterns: array(string) - Array of glob patterns to exclude
        created_at: date-time - When this sync was created
        updated_at: date-time - When this sync was last updated
        sync_interval_minutes: int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
        interval: string - If trigger is `daily`, this specifies how often to run this sync. One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        recurring_day: int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        recurring_days: array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        schedule_id: int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the sync's schedule fields.
        schedule_days_of_week: array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
        schedule_times_of_day: array(string) - Times of day to run in HH:MM format. For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
        schedule_time_zone: string - Time zone for the schedule. If not set, times are interpreted as UTC.
        holiday_region: string - Skip the sync if there is a formal, observed holiday for this region.
        latest_sync_run: SyncRun - The latest run of this sync
    """

    default_attributes = {
        "id": None,  # int64 - Sync ID
        "name": None,  # string - Name for this sync job
        "description": None,  # string - Description for this sync job
        "site_id": None,  # int64 - Site ID this sync belongs to
        "workspace_id": None,  # int64 - Workspace ID this sync belongs to
        "user_id": None,  # int64 - User who created or owns this sync
        "src_path": None,  # string - Absolute source path for the sync
        "dest_path": None,  # string - Absolute destination path for the sync
        "src_remote_server_id": None,  # int64 - Remote server ID for the source (if remote)
        "dest_remote_server_id": None,  # int64 - Remote server ID for the destination (if remote)
        "src_site_id": None,  # int64 - Source site ID if syncing from a child or partner site
        "dest_site_id": None,  # int64 - Destination site ID if syncing to a child or partner site
        "two_way": None,  # boolean - Is this a two-way sync?
        "keep_after_copy": None,  # boolean - Keep files after copying?
        "delete_empty_folders": None,  # boolean - Delete empty folders after sync?
        "disabled": None,  # boolean - Is this sync disabled?
        "trigger": None,  # string - Trigger type: daily, custom_schedule, or manual
        "trigger_file": None,  # string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
        "always_write_trigger_file": None,  # boolean - If true, the trigger file will be sent at the end of a successful sync even when no files were transferred.
        "include_patterns": None,  # array(string) - Array of glob patterns to include
        "exclude_patterns": None,  # array(string) - Array of glob patterns to exclude
        "created_at": None,  # date-time - When this sync was created
        "updated_at": None,  # date-time - When this sync was last updated
        "sync_interval_minutes": None,  # int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
        "interval": None,  # string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        "recurring_day": None,  # int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        "recurring_days": None,  # array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        "schedule_id": None,  # int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the sync's schedule fields.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
        "schedule_times_of_day": None,  # array(string) - Times of day to run in HH:MM format. For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
        "schedule_time_zone": None,  # string - Time zone for the schedule. If not set, times are interpreted as UTC.
        "holiday_region": None,  # string - Skip the sync if there is a formal, observed holiday for this region.
        "latest_sync_run": None,  # SyncRun - The latest run of this sync
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    name: str | None
    description: str | None
    site_id: int | None
    workspace_id: int | None
    user_id: int | None
    src_path: str | None
    dest_path: str | None
    src_remote_server_id: int | None
    dest_remote_server_id: int | None
    src_site_id: int | None
    dest_site_id: int | None
    two_way: bool | None
    keep_after_copy: bool | None
    delete_empty_folders: bool | None
    disabled: bool | None
    trigger: str | None
    trigger_file: str | None
    always_write_trigger_file: bool | None
    include_patterns: builtins.list[str] | None
    exclude_patterns: builtins.list[str] | None
    created_at: str | None
    updated_at: str | None
    sync_interval_minutes: int | None
    interval: str | None
    recurring_day: int | None
    recurring_days: builtins.list[int] | None
    schedule_id: int | None
    schedule_days_of_week: builtins.list[int] | None
    schedule_times_of_day: builtins.list[str] | None
    schedule_time_zone: str | None
    holiday_region: str | None
    latest_sync_run: dict[str, Any] | None

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
        for attribute, default_value in Sync.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Sync.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def dry_run(self, params: dict[str, Any] | None = None) -> None:
        """Dry Run Sync"""
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
            "POST", "/syncs/" + path_value(params["id"]) + "/dry_run", params
        )

    def manual_run(self, params: dict[str, Any] | None = None) -> None:
        """Manually Run Sync"""
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
            "/syncs/" + path_value(params["id"]) + "/manual_run",
            params,
        )

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          delete_empty_folders - boolean - Delete empty folders after sync?
          description - string - Description for this sync job
          dest_path - string - Absolute destination path for the sync
          dest_remote_server_id - int64 - Remote server ID for the destination (if remote)
          disabled - boolean - Is this sync disabled?
          exclude_patterns - array(string) - Array of glob patterns to exclude
          holiday_region - string - Skip the sync if there is a formal, observed holiday for this region.
          include_patterns - array(string) - Array of glob patterns to include
          interval - string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
          keep_after_copy - boolean - Keep files after copying?
          name - string - Name for this sync job
          recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
          recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
          schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the sync's schedule fields.
          schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
          schedule_time_zone - string - Time zone for the schedule. If not set, times are interpreted as UTC.
          schedule_times_of_day - array(string) - Times of day to run in HH:MM format. For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
          src_path - string - Absolute source path for the sync
          src_remote_server_id - int64 - Remote server ID for the source (if remote)
          sync_interval_minutes - int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
          trigger - string - Trigger type: daily, custom_schedule, or manual
          trigger_file - string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
          always_write_trigger_file - boolean - If true, the trigger file will be sent at the end of a successful sync even when no files were transferred.
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
        if "delete_empty_folders" in params and isinstance(
            params["delete_empty_folders"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: delete_empty_folders must be an bool"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "dest_path" in params and not isinstance(params["dest_path"], str):
            raise InvalidParameterError(
                "Bad parameter: dest_path must be an str"
            )
        if "dest_remote_server_id" in params and (
            not isinstance(params["dest_remote_server_id"], int)
            or isinstance(params["dest_remote_server_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: dest_remote_server_id must be an int"
            )
        if "disabled" in params and isinstance(
            params["disabled"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "exclude_patterns" in params and not isinstance(
            params["exclude_patterns"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: exclude_patterns must be an list"
            )
        if "holiday_region" in params and not isinstance(
            params["holiday_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: holiday_region must be an str"
            )
        if "include_patterns" in params and not isinstance(
            params["include_patterns"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: include_patterns must be an list"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "keep_after_copy" in params and isinstance(
            params["keep_after_copy"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: keep_after_copy must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
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
        if "src_path" in params and not isinstance(params["src_path"], str):
            raise InvalidParameterError(
                "Bad parameter: src_path must be an str"
            )
        if "src_remote_server_id" in params and (
            not isinstance(params["src_remote_server_id"], int)
            or isinstance(params["src_remote_server_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: src_remote_server_id must be an int"
            )
        if "sync_interval_minutes" in params and (
            not isinstance(params["sync_interval_minutes"], int)
            or isinstance(params["sync_interval_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: sync_interval_minutes must be an int"
            )
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "trigger_file" in params and not isinstance(
            params["trigger_file"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: trigger_file must be an str"
            )
        if "always_write_trigger_file" in params and isinstance(
            params["always_write_trigger_file"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: always_write_trigger_file must be an bool"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/syncs/" + path_value(params["id"]), params
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
            "DELETE", "/syncs/" + path_value(params["id"]), params
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
            new_obj = SyncResource(self._scope()).create(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class SyncResource:
    """Sync operations that use one client's configuration.

    Get one from a client, such as ``client.sync``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Sync]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id` or `name`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`, `disabled`, `src_remote_server_id` or `dest_remote_server_id`. Valid field combinations are `[ workspace_id, disabled ]`, `[ workspace_id, src_remote_server_id ]`, `[ workspace_id, dest_remote_server_id ]`, `[ disabled, src_remote_server_id ]`, `[ disabled, dest_remote_server_id ]`, `[ workspace_id, disabled, src_remote_server_id ]` or `[ workspace_id, disabled, dest_remote_server_id ]`.
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
        return ListObj(Sync, "GET", "/syncs", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Sync]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Sync:
        """Parameters:
        id (required) - int64 - Sync ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Sync:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/syncs/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Sync)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Sync:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Sync:
        """Parameters:
        delete_empty_folders - boolean - Delete empty folders after sync?
        description - string - Description for this sync job
        dest_path - string - Absolute destination path for the sync
        dest_remote_server_id - int64 - Remote server ID for the destination (if remote)
        disabled - boolean - Is this sync disabled?
        exclude_patterns - array(string) - Array of glob patterns to exclude
        holiday_region - string - Skip the sync if there is a formal, observed holiday for this region.
        include_patterns - array(string) - Array of glob patterns to include
        interval - string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        keep_after_copy - boolean - Keep files after copying?
        name - string - Name for this sync job
        recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the sync's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
        schedule_time_zone - string - Time zone for the schedule. If not set, times are interpreted as UTC.
        schedule_times_of_day - array(string) - Times of day to run in HH:MM format. For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
        src_path - string - Absolute source path for the sync
        src_remote_server_id - int64 - Remote server ID for the source (if remote)
        sync_interval_minutes - int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
        trigger - string - Trigger type: daily, custom_schedule, or manual
        trigger_file - string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
        always_write_trigger_file - boolean - If true, the trigger file will be sent at the end of a successful sync even when no files were transferred.
        workspace_id - int64 - Workspace ID this sync belongs to
        """
        params = copy_params(params)
        if "delete_empty_folders" in params and not isinstance(
            params["delete_empty_folders"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: delete_empty_folders must be an bool"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "dest_path" in params and not isinstance(params["dest_path"], str):
            raise InvalidParameterError(
                "Bad parameter: dest_path must be an str"
            )
        if "dest_remote_server_id" in params and (
            not isinstance(params["dest_remote_server_id"], int)
            or isinstance(params["dest_remote_server_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: dest_remote_server_id must be an int"
            )
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "exclude_patterns" in params and not isinstance(
            params["exclude_patterns"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: exclude_patterns must be an list"
            )
        if "holiday_region" in params and not isinstance(
            params["holiday_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: holiday_region must be an str"
            )
        if "include_patterns" in params and not isinstance(
            params["include_patterns"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: include_patterns must be an list"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "keep_after_copy" in params and not isinstance(
            params["keep_after_copy"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: keep_after_copy must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
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
        if "src_path" in params and not isinstance(params["src_path"], str):
            raise InvalidParameterError(
                "Bad parameter: src_path must be an str"
            )
        if "src_remote_server_id" in params and (
            not isinstance(params["src_remote_server_id"], int)
            or isinstance(params["src_remote_server_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: src_remote_server_id must be an int"
            )
        if "sync_interval_minutes" in params and (
            not isinstance(params["sync_interval_minutes"], int)
            or isinstance(params["sync_interval_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: sync_interval_minutes must be an int"
            )
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "trigger_file" in params and not isinstance(
            params["trigger_file"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: trigger_file must be an str"
            )
        if "always_write_trigger_file" in params and not isinstance(
            params["always_write_trigger_file"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: always_write_trigger_file must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/syncs", params)
        return operation.decode_model(response, Sync)

    def dry_run(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Dry Run Sync"""
        return self.__dry_run({"id": id}, params, options)

    def __dry_run(
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
            "POST", "/syncs/" + path_value(params["id"]) + "/dry_run", params
        )

    def manual_run(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Manually Run Sync"""
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
            "/syncs/" + path_value(params["id"]) + "/manual_run",
            params,
        )

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Sync:
        """Parameters:
        delete_empty_folders - boolean - Delete empty folders after sync?
        description - string - Description for this sync job
        dest_path - string - Absolute destination path for the sync
        dest_remote_server_id - int64 - Remote server ID for the destination (if remote)
        disabled - boolean - Is this sync disabled?
        exclude_patterns - array(string) - Array of glob patterns to exclude
        holiday_region - string - Skip the sync if there is a formal, observed holiday for this region.
        include_patterns - array(string) - Array of glob patterns to include
        interval - string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        keep_after_copy - boolean - Keep files after copying?
        name - string - Name for this sync job
        recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the sync's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
        schedule_time_zone - string - Time zone for the schedule. If not set, times are interpreted as UTC.
        schedule_times_of_day - array(string) - Times of day to run in HH:MM format. For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
        src_path - string - Absolute source path for the sync
        src_remote_server_id - int64 - Remote server ID for the source (if remote)
        sync_interval_minutes - int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
        trigger - string - Trigger type: daily, custom_schedule, or manual
        trigger_file - string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
        always_write_trigger_file - boolean - If true, the trigger file will be sent at the end of a successful sync even when no files were transferred.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Sync:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "delete_empty_folders" in params and not isinstance(
            params["delete_empty_folders"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: delete_empty_folders must be an bool"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "dest_path" in params and not isinstance(params["dest_path"], str):
            raise InvalidParameterError(
                "Bad parameter: dest_path must be an str"
            )
        if "dest_remote_server_id" in params and (
            not isinstance(params["dest_remote_server_id"], int)
            or isinstance(params["dest_remote_server_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: dest_remote_server_id must be an int"
            )
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "exclude_patterns" in params and not isinstance(
            params["exclude_patterns"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: exclude_patterns must be an list"
            )
        if "holiday_region" in params and not isinstance(
            params["holiday_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: holiday_region must be an str"
            )
        if "include_patterns" in params and not isinstance(
            params["include_patterns"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: include_patterns must be an list"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "keep_after_copy" in params and not isinstance(
            params["keep_after_copy"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: keep_after_copy must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
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
        if "src_path" in params and not isinstance(params["src_path"], str):
            raise InvalidParameterError(
                "Bad parameter: src_path must be an str"
            )
        if "src_remote_server_id" in params and (
            not isinstance(params["src_remote_server_id"], int)
            or isinstance(params["src_remote_server_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: src_remote_server_id must be an int"
            )
        if "sync_interval_minutes" in params and (
            not isinstance(params["sync_interval_minutes"], int)
            or isinstance(params["sync_interval_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: sync_interval_minutes must be an int"
            )
        if "trigger" in params and not isinstance(params["trigger"], str):
            raise InvalidParameterError(
                "Bad parameter: trigger must be an str"
            )
        if "trigger_file" in params and not isinstance(
            params["trigger_file"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: trigger_file must be an str"
            )
        if "always_write_trigger_file" in params and not isinstance(
            params["always_write_trigger_file"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: always_write_trigger_file must be an bool"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/syncs/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Sync)

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
            "DELETE", "/syncs/" + path_value(params["id"]), params
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
    ) -> Sync:
        """A new Sync with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Sync(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = SyncResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Sync]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id` or `name`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `workspace_id`, `disabled`, `src_remote_server_id` or `dest_remote_server_id`. Valid field combinations are `[ workspace_id, disabled ]`, `[ workspace_id, src_remote_server_id ]`, `[ workspace_id, dest_remote_server_id ]`, `[ disabled, src_remote_server_id ]`, `[ disabled, dest_remote_server_id ]`, `[ workspace_id, disabled, src_remote_server_id ]` or `[ workspace_id, disabled, dest_remote_server_id ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Sync]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Sync:
    """Parameters:
    id (required) - int64 - Sync ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Sync:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Sync:
    """Parameters:
    delete_empty_folders - boolean - Delete empty folders after sync?
    description - string - Description for this sync job
    dest_path - string - Absolute destination path for the sync
    dest_remote_server_id - int64 - Remote server ID for the destination (if remote)
    disabled - boolean - Is this sync disabled?
    exclude_patterns - array(string) - Array of glob patterns to exclude
    holiday_region - string - Skip the sync if there is a formal, observed holiday for this region.
    include_patterns - array(string) - Array of glob patterns to include
    interval - string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
    keep_after_copy - boolean - Keep files after copying?
    name - string - Name for this sync job
    recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the sync's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
    schedule_time_zone - string - Time zone for the schedule. If not set, times are interpreted as UTC.
    schedule_times_of_day - array(string) - Times of day to run in HH:MM format. For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
    src_path - string - Absolute source path for the sync
    src_remote_server_id - int64 - Remote server ID for the source (if remote)
    sync_interval_minutes - int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
    trigger - string - Trigger type: daily, custom_schedule, or manual
    trigger_file - string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
    always_write_trigger_file - boolean - If true, the trigger file will be sent at the end of a successful sync even when no files were transferred.
    workspace_id - int64 - Workspace ID this sync belongs to
    """
    return _legacy_resource.create(params, options)


def dry_run(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Dry Run Sync"""
    _legacy_resource.dry_run(id, params, options)


def manual_run(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Manually Run Sync"""
    _legacy_resource.manual_run(id, params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Sync:
    """Parameters:
    delete_empty_folders - boolean - Delete empty folders after sync?
    description - string - Description for this sync job
    dest_path - string - Absolute destination path for the sync
    dest_remote_server_id - int64 - Remote server ID for the destination (if remote)
    disabled - boolean - Is this sync disabled?
    exclude_patterns - array(string) - Array of glob patterns to exclude
    holiday_region - string - Skip the sync if there is a formal, observed holiday for this region.
    include_patterns - array(string) - Array of glob patterns to include
    interval - string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
    keep_after_copy - boolean - Keep files after copying?
    name - string - Name for this sync job
    recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the sync's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
    schedule_time_zone - string - Time zone for the schedule. If not set, times are interpreted as UTC.
    schedule_times_of_day - array(string) - Times of day to run in HH:MM format. For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
    src_path - string - Absolute source path for the sync
    src_remote_server_id - int64 - Remote server ID for the source (if remote)
    sync_interval_minutes - int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
    trigger - string - Trigger type: daily, custom_schedule, or manual
    trigger_file - string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
    always_write_trigger_file - boolean - If true, the trigger file will be sent at the end of a successful sync even when no files were transferred.
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


def new(*args, **kwargs) -> Sync:
    return Sync(*args, **kwargs)

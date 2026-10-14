import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.models.automation_authoring_schema import (
    AutomationAuthoringSchema,
)
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


class Automation:
    """A automation record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Automation ID
        workspace_id: int64 - Workspace ID
        always_serialize_jobs: boolean - Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
        always_overwrite_size_matching_files: boolean - Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer. If this flag is `true` we will overwrite the destination file always. Note that this may cause large amounts of wasted transfer usage. This setting has no effect unless `overwrite_files` is also set to `true`.
        automation: string - Automation type
        deleted: boolean - Indicates if the automation has been deleted.
        description: string - Description for the this Automation.
        definition: object - Automation v2 graph definition.
        destination_replace_from: string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
        destination_replace_to: string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
        destinations: array(string) - Destination Paths
        disabled: boolean - If true, this automation will not run.
        exclude_pattern: string - If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
        import_urls: array(object) - List of URLs to be imported and names to be used.
        inbound_email_address: string - If trigger is `email`, this is the address that triggers the Automation.
        flatten_destination_structure: boolean - Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination. If this flag is `true`, the source folder structure will be flattened in the destination. This is useful for copying or moving files from multiple folders into a single destination folder.
        group_ids: array(int64) - IDs of Groups for the Automation (i.e. who to Request File from)
        ignore_locked_folders: boolean - If true, the Lock Folders behavior will be disregarded for automated actions.
        interval: string - If trigger is `daily`, this specifies how often to run this automation. One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        last_modified_at: date-time - Time when automation was last modified. Does not change for name or description updates.
        legacy_folder_matching: boolean - If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files. This behavior no longer works and should not be used.
        name: string - Name for this automation.
        overwrite_files: boolean - If true, existing files will be overwritten with new files on Move/Copy automations. Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file. Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
        path: string - Path on which this Automation runs. Supports globs, except on remote mounts. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        path_time_zone: string - Timezone to use when rendering timestamps in paths.
        version: int64 - Current Automation v2 definition version.
        recurring_day: int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        recurring_days: array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        schedule_id: int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the automation's schedule fields.
        retry_on_failure_interval_in_minutes: int64 - If the Automation fails, retry at this interval (in minutes). Acceptable values are 5 through 1440 (one day). Set to null to disable.
        retry_on_failure_number_of_attempts: int64 - If the Automation fails, retry at most this many times. Maximum allowed value: 10. Set to null to disable.
        schedule: object - If trigger is `custom_schedule`, Custom schedule description for when the automation should be run in json format.
        human_readable_schedule: string - If trigger is `custom_schedule` or `daily` with times, Human readable schedule description for when the automation should be run.
        schedule_days_of_week: array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the automation should be run. 0 is Sunday, 1 is Monday, etc.
        schedule_times_of_day: array(string) - Times of day to run in HH:MM format (24-hour). For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
        schedule_time_zone: string - Time zone for the schedule. If not set, times are interpreted as UTC.
        source: string - Source path/glob. See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
        sync_ids: array(int64) - IDs of Syncs to run by this Automation.
        trigger_actions: array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, copy, move, archived_delete, update, read, destroy
        trigger: string - How this automation is triggered to run.
        user_id: int64 - User ID of the Automation's creator.
        user_ids: array(int64) - IDs of Users for the Automation (i.e. who to Request File from)
        value: object - A Hash of attributes specific to the automation type.
        webhook_url: string - If trigger is `webhook`, this is the URL of the webhook to trigger the Automation.
        holiday_region: string - Skip the automation if there is a formal, observed holiday for this region.
    """

    default_attributes = {
        "id": None,  # int64 - Automation ID
        "workspace_id": None,  # int64 - Workspace ID
        "always_serialize_jobs": None,  # boolean - Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
        "always_overwrite_size_matching_files": None,  # boolean - Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
        "automation": None,  # string - Automation type
        "deleted": None,  # boolean - Indicates if the automation has been deleted.
        "description": None,  # string - Description for the this Automation.
        "definition": None,  # object - Automation v2 graph definition.
        "destination_replace_from": None,  # string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
        "destination_replace_to": None,  # string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
        "destinations": None,  # array(string) - Destination Paths
        "disabled": None,  # boolean - If true, this automation will not run.
        "exclude_pattern": None,  # string - If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
        "import_urls": None,  # array(object) - List of URLs to be imported and names to be used.
        "inbound_email_address": None,  # string - If trigger is `email`, this is the address that triggers the Automation.
        "flatten_destination_structure": None,  # boolean - Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
        "group_ids": None,  # array(int64) - IDs of Groups for the Automation (i.e. who to Request File from)
        "ignore_locked_folders": None,  # boolean - If true, the Lock Folders behavior will be disregarded for automated actions.
        "interval": None,  # string - If trigger is `daily`, this specifies how often to run this automation.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        "last_modified_at": None,  # date-time - Time when automation was last modified. Does not change for name or description updates.
        "legacy_folder_matching": None,  # boolean - If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
        "name": None,  # string - Name for this automation.
        "overwrite_files": None,  # boolean - If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
        "path": None,  # string - Path on which this Automation runs.  Supports globs, except on remote mounts. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "path_time_zone": None,  # string - Timezone to use when rendering timestamps in paths.
        "version": None,  # int64 - Current Automation v2 definition version.
        "recurring_day": None,  # int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        "recurring_days": None,  # array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        "schedule_id": None,  # int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the automation's schedule fields.
        "retry_on_failure_interval_in_minutes": None,  # int64 - If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
        "retry_on_failure_number_of_attempts": None,  # int64 - If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
        "schedule": None,  # object - If trigger is `custom_schedule`, Custom schedule description for when the automation should be run in json format.
        "human_readable_schedule": None,  # string - If trigger is `custom_schedule` or `daily` with times, Human readable schedule description for when the automation should be run.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the automation should be run. 0 is Sunday, 1 is Monday, etc.
        "schedule_times_of_day": None,  # array(string) - Times of day to run in HH:MM format (24-hour). For `custom_schedule`, run at these times on specified days of week. For `daily`, run at these times on the scheduled interval date.
        "schedule_time_zone": None,  # string - Time zone for the schedule. If not set, times are interpreted as UTC.
        "source": None,  # string - Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
        "sync_ids": None,  # array(int64) - IDs of Syncs to run by this Automation.
        "trigger_actions": None,  # array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, copy, move, archived_delete, update, read, destroy
        "trigger": None,  # string - How this automation is triggered to run.
        "user_id": None,  # int64 - User ID of the Automation's creator.
        "user_ids": None,  # array(int64) - IDs of Users for the Automation (i.e. who to Request File from)
        "value": None,  # object - A Hash of attributes specific to the automation type.
        "webhook_url": None,  # string - If trigger is `webhook`, this is the URL of the webhook to trigger the Automation.
        "holiday_region": None,  # string - Skip the automation if there is a formal, observed holiday for this region.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    workspace_id: int | None
    always_serialize_jobs: bool | None
    always_overwrite_size_matching_files: bool | None
    automation: str | None
    deleted: bool | None
    description: str | None
    definition: dict[str, Any] | None
    destination_replace_from: str | None
    destination_replace_to: str | None
    destinations: builtins.list[str] | None
    disabled: bool | None
    exclude_pattern: str | None
    import_urls: builtins.list[dict[str, Any]] | None
    inbound_email_address: str | None
    flatten_destination_structure: bool | None
    group_ids: builtins.list[int] | None
    ignore_locked_folders: bool | None
    interval: str | None
    last_modified_at: str | None
    legacy_folder_matching: bool | None
    name: str | None
    overwrite_files: bool | None
    path: str | None
    path_time_zone: str | None
    version: int | None
    recurring_day: int | None
    recurring_days: builtins.list[int] | None
    schedule_id: int | None
    retry_on_failure_interval_in_minutes: int | None
    retry_on_failure_number_of_attempts: int | None
    schedule: dict[str, Any] | None
    human_readable_schedule: str | None
    schedule_days_of_week: builtins.list[int] | None
    schedule_times_of_day: builtins.list[str] | None
    schedule_time_zone: str | None
    source: str | None
    sync_ids: builtins.list[int] | None
    trigger_actions: builtins.list[str] | None
    trigger: str | None
    user_id: int | None
    user_ids: builtins.list[int] | None
    value: dict[str, Any] | None
    webhook_url: str | None
    holiday_region: str | None

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
        for attribute, default_value in Automation.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Automation.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def upgrade(self, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Upgrade a legacy Automation to Automation v2"""
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
            "/automations/" + path_value(params["id"]) + "/upgrade",
            params,
        )
        if not isinstance(response.data, dict):
            raise unexpected_response_error(
                response, "a record was not a JSON object"
            )
        return response.data

    def manual_run(self, params: dict[str, Any] | None = None) -> None:
        """Manually Run Automation

        Parameters:
          items - array(object) - Initial items for a v2 manual trigger. Each item contains exactly one `file` path or `data` object.
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
        if "items" in params and not isinstance(
            params["items"], builtins.list
        ):
            raise InvalidParameterError("Bad parameter: items must be an list")
        operation = Operation.start(self._scope())
        operation.request(
            "POST",
            "/automations/" + path_value(params["id"]) + "/manual_run",
            params,
        )

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          source - string - Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
          destinations - array(string) - A list of destination paths. Use a trailing slash for folder destinations and omit it for file destinations.
          destination_replace_from - string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
          destination_replace_to - string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
          interval - string - How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
          path - string - Path on which this Automation runs.  Supports globs, except on remote mounts.
          sync_ids - string - A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
          user_ids - string - A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
          group_ids - string - A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
          schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the automation's schedule fields.
          schedule_days_of_week - array(int64) - If trigger is `custom_schedule` without `schedule_id`, a list of days of the week to run this automation. 0 is Sunday, 1 is Monday, etc.
          schedule_times_of_day - array(string) - Times of day to run in HH:MM format (24-hour). Required for `custom_schedule` without `schedule_id`. Optional for `daily` triggers; if not set, runs at midnight UTC.
          schedule_time_zone - string - Time zone for schedule fields. Optional for `custom_schedule` without `schedule_id` and for `daily`. If not set, times are interpreted as UTC.
          holiday_region - string - Skip automation on holidays in this region. Optional for `custom_schedule` without `schedule_id` and for `daily`.
          always_overwrite_size_matching_files - boolean - Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
          always_serialize_jobs - boolean - Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
          description - string - Description for the this Automation.
          definition - object - Automation v2 graph definition.
          disabled - boolean - If true, this automation will not run.
          exclude_pattern - string - If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
          import_urls - array(object) - List of URLs to be imported and names to be used.
          flatten_destination_structure - boolean - Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
          ignore_locked_folders - boolean - If true, the Lock Folders behavior will be disregarded for automated actions.
          legacy_folder_matching - boolean - DEPRECATED: If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
          name - string - Name for this automation.
          overwrite_files - boolean - If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
          path_time_zone - string - Timezone to use when rendering timestamps in paths.
          retry_on_failure_interval_in_minutes - int64 - If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
          retry_on_failure_number_of_attempts - int64 - If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
          trigger - string - How this automation is triggered to run.
          trigger_actions - array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, copy, move, archived_delete, update, read, destroy
          value - object - A Hash of attributes specific to the automation type.
          recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
          recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
          automation - string - Automation type
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
        if "source" in params and not isinstance(params["source"], str):
            raise InvalidParameterError("Bad parameter: source must be an str")
        if "destinations" in params and not isinstance(
            params["destinations"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: destinations must be an list"
            )
        if "destination_replace_from" in params and not isinstance(
            params["destination_replace_from"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_replace_from must be an str"
            )
        if "destination_replace_to" in params and not isinstance(
            params["destination_replace_to"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_replace_to must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "sync_ids" in params and not isinstance(params["sync_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: sync_ids must be an str"
            )
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: user_ids must be an str"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
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
        if "always_overwrite_size_matching_files" in params and isinstance(
            params["always_overwrite_size_matching_files"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: always_overwrite_size_matching_files must be an bool"
            )
        if "always_serialize_jobs" in params and isinstance(
            params["always_serialize_jobs"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: always_serialize_jobs must be an bool"
            )
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
        if "exclude_pattern" in params and not isinstance(
            params["exclude_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: exclude_pattern must be an str"
            )
        if "import_urls" in params and not isinstance(
            params["import_urls"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: import_urls must be an list"
            )
        if "flatten_destination_structure" in params and isinstance(
            params["flatten_destination_structure"],
            (builtins.list, tuple, dict),
        ):
            raise InvalidParameterError(
                "Bad parameter: flatten_destination_structure must be an bool"
            )
        if "ignore_locked_folders" in params and isinstance(
            params["ignore_locked_folders"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: ignore_locked_folders must be an bool"
            )
        if "legacy_folder_matching" in params and isinstance(
            params["legacy_folder_matching"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: legacy_folder_matching must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "overwrite_files" in params and isinstance(
            params["overwrite_files"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite_files must be an bool"
            )
        if "path_time_zone" in params and not isinstance(
            params["path_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_time_zone must be an str"
            )
        if "retry_on_failure_interval_in_minutes" in params and (
            not isinstance(params["retry_on_failure_interval_in_minutes"], int)
            or isinstance(params["retry_on_failure_interval_in_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: retry_on_failure_interval_in_minutes must be an int"
            )
        if "retry_on_failure_number_of_attempts" in params and (
            not isinstance(params["retry_on_failure_number_of_attempts"], int)
            or isinstance(params["retry_on_failure_number_of_attempts"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: retry_on_failure_number_of_attempts must be an int"
            )
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
        if "automation" in params and not isinstance(
            params["automation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: automation must be an str"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/automations/" + path_value(params["id"]), params
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
            "DELETE", "/automations/" + path_value(params["id"]), params
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
            new_obj = AutomationResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class AutomationResource:
    """Automation operations that use one client's configuration.

    Get one from a client, such as ``client.automation``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Automation]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name`, `automation`, `last_modified_at` or `disabled`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `last_modified_at`, `workspace_id` or `automation`. Valid field combinations are `[ disabled, last_modified_at ]`, `[ workspace_id, disabled ]`, `[ disabled, automation ]`, `[ workspace_id, last_modified_at ]`, `[ automation, last_modified_at ]`, `[ workspace_id, automation ]`, `[ workspace_id, disabled, last_modified_at ]`, `[ disabled, automation, last_modified_at ]`, `[ workspace_id, disabled, automation ]`, `[ workspace_id, automation, last_modified_at ]` or `[ workspace_id, disabled, automation, last_modified_at ]`.
        filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `last_modified_at`.
        filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `last_modified_at`.
        filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `last_modified_at`.
        filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `last_modified_at`.
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
        if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_gt must be an dict"
            )
        if "filter_gteq" in params and not isinstance(
            params["filter_gteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_gteq must be an dict"
            )
        if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter_lt must be an dict"
            )
        if "filter_lteq" in params and not isinstance(
            params["filter_lteq"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_lteq must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(Automation, "GET", "/automations", params, operation)

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Automation]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Automation:
        """Parameters:
        id (required) - int64 - Automation ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Automation:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/automations/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Automation)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Automation:
        """The same as find()."""
        return self.find(id, params, options)

    def get_authoring_schema(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> AutomationAuthoringSchema:
        params = copy_params(params)
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/automations/authoring_schema", params
        )
        return operation.decode_model(response, AutomationAuthoringSchema)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Automation:
        """Parameters:
        source - string - Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
        destinations - array(string) - A list of destination paths. Use a trailing slash for folder destinations and omit it for file destinations.
        destination_replace_from - string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
        destination_replace_to - string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
        interval - string - How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        path - string - Path on which this Automation runs.  Supports globs, except on remote mounts.
        sync_ids - string - A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
        user_ids - string - A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
        group_ids - string - A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the automation's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule` without `schedule_id`, a list of days of the week to run this automation. 0 is Sunday, 1 is Monday, etc.
        schedule_times_of_day - array(string) - Times of day to run in HH:MM format (24-hour). Required for `custom_schedule` without `schedule_id`. Optional for `daily` triggers; if not set, runs at midnight UTC.
        schedule_time_zone - string - Time zone for schedule fields. Optional for `custom_schedule` without `schedule_id` and for `daily`. If not set, times are interpreted as UTC.
        holiday_region - string - Skip automation on holidays in this region. Optional for `custom_schedule` without `schedule_id` and for `daily`.
        always_overwrite_size_matching_files - boolean - Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
        always_serialize_jobs - boolean - Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
        description - string - Description for the this Automation.
        definition - object - Automation v2 graph definition.
        disabled - boolean - If true, this automation will not run.
        exclude_pattern - string - If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
        import_urls - array(object) - List of URLs to be imported and names to be used.
        flatten_destination_structure - boolean - Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
        ignore_locked_folders - boolean - If true, the Lock Folders behavior will be disregarded for automated actions.
        legacy_folder_matching - boolean - DEPRECATED: If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
        name - string - Name for this automation.
        overwrite_files - boolean - If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
        path_time_zone - string - Timezone to use when rendering timestamps in paths.
        retry_on_failure_interval_in_minutes - int64 - If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
        retry_on_failure_number_of_attempts - int64 - If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
        trigger - string - How this automation is triggered to run.
        trigger_actions - array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, copy, move, archived_delete, update, read, destroy
        value - object - A Hash of attributes specific to the automation type.
        recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        automation (required) - string - Automation type
        workspace_id - int64 - Workspace ID
        """
        params = copy_params(params)
        if "source" in params and not isinstance(params["source"], str):
            raise InvalidParameterError("Bad parameter: source must be an str")
        if "destinations" in params and not isinstance(
            params["destinations"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: destinations must be an list"
            )
        if "destination_replace_from" in params and not isinstance(
            params["destination_replace_from"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_replace_from must be an str"
            )
        if "destination_replace_to" in params and not isinstance(
            params["destination_replace_to"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_replace_to must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "sync_ids" in params and not isinstance(params["sync_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: sync_ids must be an str"
            )
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: user_ids must be an str"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
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
        if (
            "always_overwrite_size_matching_files" in params
            and not isinstance(
                params["always_overwrite_size_matching_files"], bool
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: always_overwrite_size_matching_files must be an bool"
            )
        if "always_serialize_jobs" in params and not isinstance(
            params["always_serialize_jobs"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: always_serialize_jobs must be an bool"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "definition" in params and not isinstance(
            params["definition"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: definition must be an dict"
            )
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "exclude_pattern" in params and not isinstance(
            params["exclude_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: exclude_pattern must be an str"
            )
        if "import_urls" in params and not isinstance(
            params["import_urls"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: import_urls must be an list"
            )
        if "flatten_destination_structure" in params and not isinstance(
            params["flatten_destination_structure"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: flatten_destination_structure must be an bool"
            )
        if "ignore_locked_folders" in params and not isinstance(
            params["ignore_locked_folders"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ignore_locked_folders must be an bool"
            )
        if "legacy_folder_matching" in params and not isinstance(
            params["legacy_folder_matching"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: legacy_folder_matching must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "overwrite_files" in params and not isinstance(
            params["overwrite_files"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite_files must be an bool"
            )
        if "path_time_zone" in params and not isinstance(
            params["path_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_time_zone must be an str"
            )
        if "retry_on_failure_interval_in_minutes" in params and (
            not isinstance(params["retry_on_failure_interval_in_minutes"], int)
            or isinstance(params["retry_on_failure_interval_in_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: retry_on_failure_interval_in_minutes must be an int"
            )
        if "retry_on_failure_number_of_attempts" in params and (
            not isinstance(params["retry_on_failure_number_of_attempts"], int)
            or isinstance(params["retry_on_failure_number_of_attempts"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: retry_on_failure_number_of_attempts must be an int"
            )
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
        if "value" in params and not isinstance(params["value"], dict):
            raise InvalidParameterError("Bad parameter: value must be an dict")
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
        if "automation" in params and not isinstance(
            params["automation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: automation must be an str"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "automation" not in params:
            raise MissingParameterError("Parameter missing: automation")
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/automations", params)
        return operation.decode_model(response, Automation)

    def upgrade(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Automation:
        """Upgrade a legacy Automation to Automation v2"""
        return self.__upgrade({"id": id}, params, options)

    def __upgrade(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Automation:
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
            "/automations/" + path_value(params["id"]) + "/upgrade",
            params,
        )
        return operation.decode_model(response, Automation)

    def manual_run(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """Manually Run Automation

        Parameters:
          items - array(object) - Initial items for a v2 manual trigger. Each item contains exactly one `file` path or `data` object.
        """
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
        if "items" in params and not isinstance(
            params["items"], builtins.list
        ):
            raise InvalidParameterError("Bad parameter: items must be an list")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "POST",
            "/automations/" + path_value(params["id"]) + "/manual_run",
            params,
        )

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Automation:
        """Parameters:
        source - string - Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
        destinations - array(string) - A list of destination paths. Use a trailing slash for folder destinations and omit it for file destinations.
        destination_replace_from - string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
        destination_replace_to - string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
        interval - string - How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        path - string - Path on which this Automation runs.  Supports globs, except on remote mounts.
        sync_ids - string - A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
        user_ids - string - A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
        group_ids - string - A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
        schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the automation's schedule fields.
        schedule_days_of_week - array(int64) - If trigger is `custom_schedule` without `schedule_id`, a list of days of the week to run this automation. 0 is Sunday, 1 is Monday, etc.
        schedule_times_of_day - array(string) - Times of day to run in HH:MM format (24-hour). Required for `custom_schedule` without `schedule_id`. Optional for `daily` triggers; if not set, runs at midnight UTC.
        schedule_time_zone - string - Time zone for schedule fields. Optional for `custom_schedule` without `schedule_id` and for `daily`. If not set, times are interpreted as UTC.
        holiday_region - string - Skip automation on holidays in this region. Optional for `custom_schedule` without `schedule_id` and for `daily`.
        always_overwrite_size_matching_files - boolean - Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
        always_serialize_jobs - boolean - Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
        description - string - Description for the this Automation.
        definition - object - Automation v2 graph definition.
        disabled - boolean - If true, this automation will not run.
        exclude_pattern - string - If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
        import_urls - array(object) - List of URLs to be imported and names to be used.
        flatten_destination_structure - boolean - Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
        ignore_locked_folders - boolean - If true, the Lock Folders behavior will be disregarded for automated actions.
        legacy_folder_matching - boolean - DEPRECATED: If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
        name - string - Name for this automation.
        overwrite_files - boolean - If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
        path_time_zone - string - Timezone to use when rendering timestamps in paths.
        retry_on_failure_interval_in_minutes - int64 - If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
        retry_on_failure_number_of_attempts - int64 - If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
        trigger - string - How this automation is triggered to run.
        trigger_actions - array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, copy, move, archived_delete, update, read, destroy
        value - object - A Hash of attributes specific to the automation type.
        recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        automation - string - Automation type
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Automation:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "source" in params and not isinstance(params["source"], str):
            raise InvalidParameterError("Bad parameter: source must be an str")
        if "destinations" in params and not isinstance(
            params["destinations"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: destinations must be an list"
            )
        if "destination_replace_from" in params and not isinstance(
            params["destination_replace_from"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_replace_from must be an str"
            )
        if "destination_replace_to" in params and not isinstance(
            params["destination_replace_to"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: destination_replace_to must be an str"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "sync_ids" in params and not isinstance(params["sync_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: sync_ids must be an str"
            )
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: user_ids must be an str"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
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
        if (
            "always_overwrite_size_matching_files" in params
            and not isinstance(
                params["always_overwrite_size_matching_files"], bool
            )
        ):
            raise InvalidParameterError(
                "Bad parameter: always_overwrite_size_matching_files must be an bool"
            )
        if "always_serialize_jobs" in params and not isinstance(
            params["always_serialize_jobs"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: always_serialize_jobs must be an bool"
            )
        if "description" in params and not isinstance(
            params["description"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: description must be an str"
            )
        if "definition" in params and not isinstance(
            params["definition"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: definition must be an dict"
            )
        if "disabled" in params and not isinstance(params["disabled"], bool):
            raise InvalidParameterError(
                "Bad parameter: disabled must be an bool"
            )
        if "exclude_pattern" in params and not isinstance(
            params["exclude_pattern"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: exclude_pattern must be an str"
            )
        if "import_urls" in params and not isinstance(
            params["import_urls"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: import_urls must be an list"
            )
        if "flatten_destination_structure" in params and not isinstance(
            params["flatten_destination_structure"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: flatten_destination_structure must be an bool"
            )
        if "ignore_locked_folders" in params and not isinstance(
            params["ignore_locked_folders"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: ignore_locked_folders must be an bool"
            )
        if "legacy_folder_matching" in params and not isinstance(
            params["legacy_folder_matching"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: legacy_folder_matching must be an bool"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "overwrite_files" in params and not isinstance(
            params["overwrite_files"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: overwrite_files must be an bool"
            )
        if "path_time_zone" in params and not isinstance(
            params["path_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: path_time_zone must be an str"
            )
        if "retry_on_failure_interval_in_minutes" in params and (
            not isinstance(params["retry_on_failure_interval_in_minutes"], int)
            or isinstance(params["retry_on_failure_interval_in_minutes"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: retry_on_failure_interval_in_minutes must be an int"
            )
        if "retry_on_failure_number_of_attempts" in params and (
            not isinstance(params["retry_on_failure_number_of_attempts"], int)
            or isinstance(params["retry_on_failure_number_of_attempts"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: retry_on_failure_number_of_attempts must be an int"
            )
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
        if "value" in params and not isinstance(params["value"], dict):
            raise InvalidParameterError("Bad parameter: value must be an dict")
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
        if "automation" in params and not isinstance(
            params["automation"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: automation must be an str"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/automations/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Automation)

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
            "DELETE", "/automations/" + path_value(params["id"]), params
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
    ) -> Automation:
        """A new Automation with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Automation(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = AutomationResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Automation]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name`, `automation`, `last_modified_at` or `disabled`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `last_modified_at`, `workspace_id` or `automation`. Valid field combinations are `[ disabled, last_modified_at ]`, `[ workspace_id, disabled ]`, `[ disabled, automation ]`, `[ workspace_id, last_modified_at ]`, `[ automation, last_modified_at ]`, `[ workspace_id, automation ]`, `[ workspace_id, disabled, last_modified_at ]`, `[ disabled, automation, last_modified_at ]`, `[ workspace_id, disabled, automation ]`, `[ workspace_id, automation, last_modified_at ]` or `[ workspace_id, disabled, automation, last_modified_at ]`.
    filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `last_modified_at`.
    filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `last_modified_at`.
    filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `last_modified_at`.
    filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `last_modified_at`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Automation]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Automation:
    """Parameters:
    id (required) - int64 - Automation ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Automation:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def get_authoring_schema(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> AutomationAuthoringSchema:
    return _legacy_resource.get_authoring_schema(params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Automation:
    """Parameters:
    source - string - Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
    destinations - array(string) - A list of destination paths. Use a trailing slash for folder destinations and omit it for file destinations.
    destination_replace_from - string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
    destination_replace_to - string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
    interval - string - How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
    path - string - Path on which this Automation runs.  Supports globs, except on remote mounts.
    sync_ids - string - A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    user_ids - string - A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    group_ids - string - A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the automation's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule` without `schedule_id`, a list of days of the week to run this automation. 0 is Sunday, 1 is Monday, etc.
    schedule_times_of_day - array(string) - Times of day to run in HH:MM format (24-hour). Required for `custom_schedule` without `schedule_id`. Optional for `daily` triggers; if not set, runs at midnight UTC.
    schedule_time_zone - string - Time zone for schedule fields. Optional for `custom_schedule` without `schedule_id` and for `daily`. If not set, times are interpreted as UTC.
    holiday_region - string - Skip automation on holidays in this region. Optional for `custom_schedule` without `schedule_id` and for `daily`.
    always_overwrite_size_matching_files - boolean - Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
    always_serialize_jobs - boolean - Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
    description - string - Description for the this Automation.
    definition - object - Automation v2 graph definition.
    disabled - boolean - If true, this automation will not run.
    exclude_pattern - string - If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
    import_urls - array(object) - List of URLs to be imported and names to be used.
    flatten_destination_structure - boolean - Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
    ignore_locked_folders - boolean - If true, the Lock Folders behavior will be disregarded for automated actions.
    legacy_folder_matching - boolean - DEPRECATED: If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
    name - string - Name for this automation.
    overwrite_files - boolean - If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
    path_time_zone - string - Timezone to use when rendering timestamps in paths.
    retry_on_failure_interval_in_minutes - int64 - If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
    retry_on_failure_number_of_attempts - int64 - If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
    trigger - string - How this automation is triggered to run.
    trigger_actions - array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, copy, move, archived_delete, update, read, destroy
    value - object - A Hash of attributes specific to the automation type.
    recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    automation (required) - string - Automation type
    workspace_id - int64 - Workspace ID
    """
    return _legacy_resource.create(params, options)


def upgrade(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Automation:
    """Upgrade a legacy Automation to Automation v2"""
    return _legacy_resource.upgrade(id, params, options)


def manual_run(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """Manually Run Automation

    Parameters:
      items - array(object) - Initial items for a v2 manual trigger. Each item contains exactly one `file` path or `data` object.
    """
    _legacy_resource.manual_run(id, params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Automation:
    """Parameters:
    source - string - Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
    destinations - array(string) - A list of destination paths. Use a trailing slash for folder destinations and omit it for file destinations.
    destination_replace_from - string - If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
    destination_replace_to - string - If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
    interval - string - How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
    path - string - Path on which this Automation runs.  Supports globs, except on remote mounts.
    sync_ids - string - A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    user_ids - string - A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    group_ids - string - A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
    schedule_id - int64 - If trigger is `custom_schedule`, the reusable Schedule used instead of the automation's schedule fields.
    schedule_days_of_week - array(int64) - If trigger is `custom_schedule` without `schedule_id`, a list of days of the week to run this automation. 0 is Sunday, 1 is Monday, etc.
    schedule_times_of_day - array(string) - Times of day to run in HH:MM format (24-hour). Required for `custom_schedule` without `schedule_id`. Optional for `daily` triggers; if not set, runs at midnight UTC.
    schedule_time_zone - string - Time zone for schedule fields. Optional for `custom_schedule` without `schedule_id` and for `daily`. If not set, times are interpreted as UTC.
    holiday_region - string - Skip automation on holidays in this region. Optional for `custom_schedule` without `schedule_id` and for `daily`.
    always_overwrite_size_matching_files - boolean - Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
    always_serialize_jobs - boolean - Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
    description - string - Description for the this Automation.
    definition - object - Automation v2 graph definition.
    disabled - boolean - If true, this automation will not run.
    exclude_pattern - string - If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
    import_urls - array(object) - List of URLs to be imported and names to be used.
    flatten_destination_structure - boolean - Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
    ignore_locked_folders - boolean - If true, the Lock Folders behavior will be disregarded for automated actions.
    legacy_folder_matching - boolean - DEPRECATED: If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
    name - string - Name for this automation.
    overwrite_files - boolean - If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
    path_time_zone - string - Timezone to use when rendering timestamps in paths.
    retry_on_failure_interval_in_minutes - int64 - If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
    retry_on_failure_number_of_attempts - int64 - If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
    trigger - string - How this automation is triggered to run.
    trigger_actions - array(string) - If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, copy, move, archived_delete, update, read, destroy
    value - object - A Hash of attributes specific to the automation type.
    recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    recurring_days - array(int64) - If trigger type is `daily`, this specifies one or more day numbers to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    automation - string - Automation type
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


def new(*args, **kwargs) -> Automation:
    return Automation(*args, **kwargs)

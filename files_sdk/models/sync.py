import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Sync:
    default_attributes = {
        "id": None,  # int64 - Sync ID
        "name": None,  # string - Name for this sync job
        "description": None,  # string - Description for this sync job
        "site_id": None,  # int64 - Site ID this sync belongs to
        "user_id": None,  # int64 - User who created or owns this sync
        "src_path": None,  # string - Absolute source path for the sync
        "dest_path": None,  # string - Absolute destination path for the sync
        "src_remote_server_id": None,  # int64 - Remote server ID for the source (if remote)
        "dest_remote_server_id": None,  # int64 - Remote server ID for the destination (if remote)
        "two_way": None,  # boolean - Is this a two-way sync?
        "keep_after_copy": None,  # boolean - Keep files after copying?
        "delete_empty_folders": None,  # boolean - Delete empty folders after sync?
        "disabled": None,  # boolean - Is this sync disabled?
        "trigger": None,  # string - Trigger type: daily, custom_schedule, or manual
        "trigger_file": None,  # string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
        "include_patterns": None,  # array(string) - Array of glob patterns to include
        "exclude_patterns": None,  # array(string) - Array of glob patterns to exclude
        "created_at": None,  # date-time - When this sync was created
        "updated_at": None,  # date-time - When this sync was last updated
        "sync_interval_minutes": None,  # int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
        "interval": None,  # string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
        "recurring_day": None,  # int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
        "schedule_days_of_week": None,  # array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
        "schedule_times_of_day": None,  # array(string) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. Times of day in HH:MM format.
        "schedule_time_zone": None,  # string - If trigger is `custom_schedule`, Custom schedule Time Zone for when the sync should be run.
        "holiday_region": None,  # string - If trigger is `custom_schedule`, the sync will check if there is a formal, observed holiday for the region, and if so, it will not run.
        "latest_sync_run": None,  # SyncRun - The latest run of this sync
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Sync.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Sync.default_attributes
            if getattr(self, k, None) is not None
        }

    # Dry Run Sync
    def dry_run(self, params=None):
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
            "/syncs/{id}/dry_run".format(id=params["id"]),
            params,
            self.options,
        )

    # Manually Run Sync
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
            "/syncs/{id}/manual_run".format(id=params["id"]),
            params,
            self.options,
        )

    # Parameters:
    #   name - string - Name for this sync job
    #   description - string - Description for this sync job
    #   src_path - string - Absolute source path
    #   dest_path - string - Absolute destination path
    #   src_remote_server_id - int64 - Remote server ID for the source
    #   dest_remote_server_id - int64 - Remote server ID for the destination
    #   keep_after_copy - boolean - Keep files after copying?
    #   delete_empty_folders - boolean - Delete empty folders after sync?
    #   disabled - boolean - Is this sync disabled?
    #   interval - string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
    #   trigger - string - Trigger type: daily, custom_schedule, or manual
    #   trigger_file - string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
    #   holiday_region - string - If trigger is `custom_schedule`, the sync will check if there is a formal, observed holiday for the region, and if so, it will not run.
    #   sync_interval_minutes - int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
    #   recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
    #   schedule_time_zone - string - If trigger is `custom_schedule`, Custom schedule Time Zone for when the sync should be run.
    #   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
    #   schedule_times_of_day - array(string) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. Times of day in HH:MM format.
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
        if "src_path" in params and not isinstance(params["src_path"], str):
            raise InvalidParameterError(
                "Bad parameter: src_path must be an str"
            )
        if "dest_path" in params and not isinstance(params["dest_path"], str):
            raise InvalidParameterError(
                "Bad parameter: dest_path must be an str"
            )
        if "src_remote_server_id" in params and not isinstance(
            params["src_remote_server_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: src_remote_server_id must be an int"
            )
        if "dest_remote_server_id" in params and not isinstance(
            params["dest_remote_server_id"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: dest_remote_server_id must be an int"
            )
        if "interval" in params and not isinstance(params["interval"], str):
            raise InvalidParameterError(
                "Bad parameter: interval must be an str"
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
        if "holiday_region" in params and not isinstance(
            params["holiday_region"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: holiday_region must be an str"
            )
        if "sync_interval_minutes" in params and not isinstance(
            params["sync_interval_minutes"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: sync_interval_minutes must be an int"
            )
        if "recurring_day" in params and not isinstance(
            params["recurring_day"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: recurring_day must be an int"
            )
        if "schedule_time_zone" in params and not isinstance(
            params["schedule_time_zone"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: schedule_time_zone must be an str"
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
        response, _options = Api.send_request(
            "PATCH",
            "/syncs/{id}".format(id=params["id"]),
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
            "/syncs/{id}".format(id=params["id"]),
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
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `src_remote_server_id` and `dest_remote_server_id`.
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
    return ListObj(Sync, "GET", "/syncs", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Sync ID.
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
        "GET", "/syncs/{id}".format(id=params["id"]), params, options
    )
    return Sync(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   name - string - Name for this sync job
#   description - string - Description for this sync job
#   src_path - string - Absolute source path
#   dest_path - string - Absolute destination path
#   src_remote_server_id - int64 - Remote server ID for the source
#   dest_remote_server_id - int64 - Remote server ID for the destination
#   keep_after_copy - boolean - Keep files after copying?
#   delete_empty_folders - boolean - Delete empty folders after sync?
#   disabled - boolean - Is this sync disabled?
#   interval - string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
#   trigger - string - Trigger type: daily, custom_schedule, or manual
#   trigger_file - string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
#   holiday_region - string - If trigger is `custom_schedule`, the sync will check if there is a formal, observed holiday for the region, and if so, it will not run.
#   sync_interval_minutes - int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
#   recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
#   schedule_time_zone - string - If trigger is `custom_schedule`, Custom schedule Time Zone for when the sync should be run.
#   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
#   schedule_times_of_day - array(string) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. Times of day in HH:MM format.
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
    if "src_path" in params and not isinstance(params["src_path"], str):
        raise InvalidParameterError("Bad parameter: src_path must be an str")
    if "dest_path" in params and not isinstance(params["dest_path"], str):
        raise InvalidParameterError("Bad parameter: dest_path must be an str")
    if "src_remote_server_id" in params and not isinstance(
        params["src_remote_server_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: src_remote_server_id must be an int"
        )
    if "dest_remote_server_id" in params and not isinstance(
        params["dest_remote_server_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: dest_remote_server_id must be an int"
        )
    if "keep_after_copy" in params and not isinstance(
        params["keep_after_copy"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: keep_after_copy must be an bool"
        )
    if "delete_empty_folders" in params and not isinstance(
        params["delete_empty_folders"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: delete_empty_folders must be an bool"
        )
    if "disabled" in params and not isinstance(params["disabled"], bool):
        raise InvalidParameterError("Bad parameter: disabled must be an bool")
    if "interval" in params and not isinstance(params["interval"], str):
        raise InvalidParameterError("Bad parameter: interval must be an str")
    if "trigger" in params and not isinstance(params["trigger"], str):
        raise InvalidParameterError("Bad parameter: trigger must be an str")
    if "trigger_file" in params and not isinstance(
        params["trigger_file"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: trigger_file must be an str"
        )
    if "holiday_region" in params and not isinstance(
        params["holiday_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: holiday_region must be an str"
        )
    if "sync_interval_minutes" in params and not isinstance(
        params["sync_interval_minutes"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: sync_interval_minutes must be an int"
        )
    if "recurring_day" in params and not isinstance(
        params["recurring_day"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: recurring_day must be an int"
        )
    if "schedule_time_zone" in params and not isinstance(
        params["schedule_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_time_zone must be an str"
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
    response, options = Api.send_request("POST", "/syncs", params, options)
    return Sync(response.data, options)


# Dry Run Sync
def dry_run(id, params=None, options=None):
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
        "POST", "/syncs/{id}/dry_run".format(id=params["id"]), params, options
    )


# Manually Run Sync
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
        "/syncs/{id}/manual_run".format(id=params["id"]),
        params,
        options,
    )


# Parameters:
#   name - string - Name for this sync job
#   description - string - Description for this sync job
#   src_path - string - Absolute source path
#   dest_path - string - Absolute destination path
#   src_remote_server_id - int64 - Remote server ID for the source
#   dest_remote_server_id - int64 - Remote server ID for the destination
#   keep_after_copy - boolean - Keep files after copying?
#   delete_empty_folders - boolean - Delete empty folders after sync?
#   disabled - boolean - Is this sync disabled?
#   interval - string - If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
#   trigger - string - Trigger type: daily, custom_schedule, or manual
#   trigger_file - string - Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
#   holiday_region - string - If trigger is `custom_schedule`, the sync will check if there is a formal, observed holiday for the region, and if so, it will not run.
#   sync_interval_minutes - int64 - Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
#   recurring_day - int64 - If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
#   schedule_time_zone - string - If trigger is `custom_schedule`, Custom schedule Time Zone for when the sync should be run.
#   schedule_days_of_week - array(int64) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
#   schedule_times_of_day - array(string) - If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. Times of day in HH:MM format.
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
    if "src_path" in params and not isinstance(params["src_path"], str):
        raise InvalidParameterError("Bad parameter: src_path must be an str")
    if "dest_path" in params and not isinstance(params["dest_path"], str):
        raise InvalidParameterError("Bad parameter: dest_path must be an str")
    if "src_remote_server_id" in params and not isinstance(
        params["src_remote_server_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: src_remote_server_id must be an int"
        )
    if "dest_remote_server_id" in params and not isinstance(
        params["dest_remote_server_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: dest_remote_server_id must be an int"
        )
    if "keep_after_copy" in params and not isinstance(
        params["keep_after_copy"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: keep_after_copy must be an bool"
        )
    if "delete_empty_folders" in params and not isinstance(
        params["delete_empty_folders"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: delete_empty_folders must be an bool"
        )
    if "disabled" in params and not isinstance(params["disabled"], bool):
        raise InvalidParameterError("Bad parameter: disabled must be an bool")
    if "interval" in params and not isinstance(params["interval"], str):
        raise InvalidParameterError("Bad parameter: interval must be an str")
    if "trigger" in params and not isinstance(params["trigger"], str):
        raise InvalidParameterError("Bad parameter: trigger must be an str")
    if "trigger_file" in params and not isinstance(
        params["trigger_file"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: trigger_file must be an str"
        )
    if "holiday_region" in params and not isinstance(
        params["holiday_region"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: holiday_region must be an str"
        )
    if "sync_interval_minutes" in params and not isinstance(
        params["sync_interval_minutes"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: sync_interval_minutes must be an int"
        )
    if "recurring_day" in params and not isinstance(
        params["recurring_day"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: recurring_day must be an int"
        )
    if "schedule_time_zone" in params and not isinstance(
        params["schedule_time_zone"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: schedule_time_zone must be an str"
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
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/syncs/{id}".format(id=params["id"]), params, options
    )
    return Sync(response.data, options)


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
        "DELETE", "/syncs/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Sync(*args, **kwargs)

import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class SyncRun:
    default_attributes = {
        "id": None,  # int64 - SyncRun ID
        "body": None,  # string - Log or summary body for this run
        "bytes_synced": None,  # int64 - Total bytes synced in this run
        "compared_files": None,  # int64 - Number of files compared
        "compared_folders": None,  # int64 - Number of folders compared
        "completed_at": None,  # date-time - When this run was completed
        "created_at": None,  # date-time - When this run was created
        "dest_remote_server_type": None,  # string - Destination remote server type, if any
        "dry_run": None,  # boolean - Whether this run was a dry run (no actual changes made)
        "errored_files": None,  # int64 - Number of files that errored
        "estimated_bytes_count": None,  # int64 - Estimated bytes count for this run
        "event_errors": None,  # array(string) - Array of errors encountered during the run
        "log_url": None,  # string - Link to external log file.
        "runtime": None,  # double - Total runtime in seconds
        "site_id": None,  # int64 - Site ID
        "src_remote_server_type": None,  # string - Source remote server type, if any
        "status": None,  # string - Status of the sync run (success, failure, partial_failure, in_progress, skipped)
        "successful_files": None,  # int64 - Number of files successfully synced
        "sync_id": None,  # int64 - ID of the Sync this run belongs to
        "sync_name": None,  # string - Name of the Sync this run belongs to
        "updated_at": None,  # date-time - When this run was last updated
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in SyncRun.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in SyncRun.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `sync_id`, `created_at` or `status`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `status`, `dry_run`, `src_remote_server_type`, `dest_remote_server_type` or `sync_id`. Valid field combinations are `[ status, created_at ]`, `[ src_remote_server_type, created_at ]`, `[ dest_remote_server_type, created_at ]`, `[ sync_id, created_at ]`, `[ src_remote_server_type, status ]`, `[ dest_remote_server_type, status ]`, `[ sync_id, status ]`, `[ src_remote_server_type, status, created_at ]`, `[ dest_remote_server_type, status, created_at ]` or `[ sync_id, status, created_at ]`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
        raise InvalidParameterError("Bad parameter: filter_gt must be an dict")
    if "filter_gteq" in params and not isinstance(params["filter_gteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_gteq must be an dict"
        )
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_lteq must be an dict"
        )
    return ListObj(SyncRun, "GET", "/sync_runs", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Sync Run ID.
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
        "GET", "/sync_runs/{id}".format(id=params["id"]), params, options
    )
    return SyncRun(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


def new(*args, **kwargs):
    return SyncRun(*args, **kwargs)

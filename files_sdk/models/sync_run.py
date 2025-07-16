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
        "sync_id": None,  # int64 - ID of the Sync this run belongs to
        "site_id": None,  # int64 - Site ID
        "status": None,  # string - Status of the sync run (success, failure, partial_failure, in_progress, skipped)
        "src_remote_server_type": None,  # string - Source remote server type, if any
        "dest_remote_server_type": None,  # string - Destination remote server type, if any
        "body": None,  # string - Log or summary body for this run
        "event_errors": None,  # array(string) - Array of errors encountered during the run
        "bytes_synced": None,  # int64 - Total bytes synced in this run
        "compared_files": None,  # int64 - Number of files compared
        "compared_folders": None,  # int64 - Number of folders compared
        "errored_files": None,  # int64 - Number of files that errored
        "successful_files": None,  # int64 - Number of files successfully synced
        "runtime": None,  # double - Total runtime in seconds
        "log_url": None,  # string - Link to external log file.
        "completed_at": None,  # date-time - When this run was completed
        "notified": None,  # boolean - Whether notifications were sent for this run
        "created_at": None,  # date-time - When this run was created
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
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `sync_id`, `created_at` or `status`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `status` and `sync_id`. Valid field combinations are `[ sync_id, status ]`.
#   sync_id (required) - int64 - ID of the Sync this run belongs to
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
    if "sync_id" in params and not isinstance(params["sync_id"], int):
        raise InvalidParameterError("Bad parameter: sync_id must be an int")
    if "sync_id" not in params:
        raise MissingParameterError("Parameter missing: sync_id")
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

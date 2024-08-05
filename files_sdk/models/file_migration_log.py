import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class FileMigrationLog:
    default_attributes = {
        "timestamp": None,  # date-time - Start Time of Action
        "file_migration_id": None,  # int64 - File Migration ID
        "dest_path": None,  # string - Destination path, for moves and copies
        "error_type": None,  # string - Error type, if applicable
        "message": None,  # string - Message
        "operation": None,  # string - Operation type
        "path": None,  # string - File path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "status": None,  # string - Status
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in FileMigrationLog.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in FileMigrationLog.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `start_date`, `end_date`, `file_migration_id`, `operation`, `status` or `type`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ file_migration_id ]`, `[ operation ]`, `[ status ]`, `[ type ]`, `[ start_date, end_date ]`, `[ start_date, file_migration_id ]`, `[ start_date, operation ]`, `[ start_date, status ]`, `[ start_date, type ]`, `[ end_date, file_migration_id ]`, `[ end_date, operation ]`, `[ end_date, status ]`, `[ end_date, type ]`, `[ file_migration_id, operation ]`, `[ file_migration_id, status ]`, `[ file_migration_id, type ]`, `[ operation, status ]`, `[ operation, type ]`, `[ status, type ]`, `[ start_date, end_date, file_migration_id ]`, `[ start_date, end_date, operation ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, type ]`, `[ start_date, file_migration_id, operation ]`, `[ start_date, file_migration_id, status ]`, `[ start_date, file_migration_id, type ]`, `[ start_date, operation, status ]`, `[ start_date, operation, type ]`, `[ start_date, status, type ]`, `[ end_date, file_migration_id, operation ]`, `[ end_date, file_migration_id, status ]`, `[ end_date, file_migration_id, type ]`, `[ end_date, operation, status ]`, `[ end_date, operation, type ]`, `[ end_date, status, type ]`, `[ file_migration_id, operation, status ]`, `[ file_migration_id, operation, type ]`, `[ file_migration_id, status, type ]`, `[ operation, status, type ]`, `[ start_date, end_date, file_migration_id, operation ]`, `[ start_date, end_date, file_migration_id, status ]`, `[ start_date, end_date, file_migration_id, type ]`, `[ start_date, end_date, operation, status ]`, `[ start_date, end_date, operation, type ]`, `[ start_date, end_date, status, type ]`, `[ start_date, file_migration_id, operation, status ]`, `[ start_date, file_migration_id, operation, type ]`, `[ start_date, file_migration_id, status, type ]`, `[ start_date, operation, status, type ]`, `[ end_date, file_migration_id, operation, status ]`, `[ end_date, file_migration_id, operation, type ]`, `[ end_date, file_migration_id, status, type ]`, `[ end_date, operation, status, type ]`, `[ file_migration_id, operation, status, type ]`, `[ start_date, end_date, file_migration_id, operation, status ]`, `[ start_date, end_date, file_migration_id, operation, type ]`, `[ start_date, end_date, file_migration_id, status, type ]`, `[ start_date, end_date, operation, status, type ]`, `[ start_date, file_migration_id, operation, status, type ]` or `[ end_date, file_migration_id, operation, status, type ]`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `operation` and `status`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ file_migration_id ]`, `[ operation ]`, `[ status ]`, `[ type ]`, `[ start_date, end_date ]`, `[ start_date, file_migration_id ]`, `[ start_date, operation ]`, `[ start_date, status ]`, `[ start_date, type ]`, `[ end_date, file_migration_id ]`, `[ end_date, operation ]`, `[ end_date, status ]`, `[ end_date, type ]`, `[ file_migration_id, operation ]`, `[ file_migration_id, status ]`, `[ file_migration_id, type ]`, `[ operation, status ]`, `[ operation, type ]`, `[ status, type ]`, `[ start_date, end_date, file_migration_id ]`, `[ start_date, end_date, operation ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, type ]`, `[ start_date, file_migration_id, operation ]`, `[ start_date, file_migration_id, status ]`, `[ start_date, file_migration_id, type ]`, `[ start_date, operation, status ]`, `[ start_date, operation, type ]`, `[ start_date, status, type ]`, `[ end_date, file_migration_id, operation ]`, `[ end_date, file_migration_id, status ]`, `[ end_date, file_migration_id, type ]`, `[ end_date, operation, status ]`, `[ end_date, operation, type ]`, `[ end_date, status, type ]`, `[ file_migration_id, operation, status ]`, `[ file_migration_id, operation, type ]`, `[ file_migration_id, status, type ]`, `[ operation, status, type ]`, `[ start_date, end_date, file_migration_id, operation ]`, `[ start_date, end_date, file_migration_id, status ]`, `[ start_date, end_date, file_migration_id, type ]`, `[ start_date, end_date, operation, status ]`, `[ start_date, end_date, operation, type ]`, `[ start_date, end_date, status, type ]`, `[ start_date, file_migration_id, operation, status ]`, `[ start_date, file_migration_id, operation, type ]`, `[ start_date, file_migration_id, status, type ]`, `[ start_date, operation, status, type ]`, `[ end_date, file_migration_id, operation, status ]`, `[ end_date, file_migration_id, operation, type ]`, `[ end_date, file_migration_id, status, type ]`, `[ end_date, operation, status, type ]`, `[ file_migration_id, operation, status, type ]`, `[ start_date, end_date, file_migration_id, operation, status ]`, `[ start_date, end_date, file_migration_id, operation, type ]`, `[ start_date, end_date, file_migration_id, status, type ]`, `[ start_date, end_date, operation, status, type ]`, `[ start_date, file_migration_id, operation, status, type ]` or `[ end_date, file_migration_id, operation, status, type ]`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    return ListObj(
        FileMigrationLog, "GET", "/file_migration_logs", params, options
    )


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return FileMigrationLog(*args, **kwargs)

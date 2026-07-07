import builtins  # noqa: F401
from urllib.parse import quote
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class FileMigration:
    default_attributes = {
        "id": None,  # int64 - File migration ID
        "path": None,  # string - Source path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "dest_path": None,  # string - Destination path
        "failure_message": None,  # string - Reason for the failure, if applicable.
        "files_moved": None,  # int64 - Number of files processed
        "files_total": None,  # int64
        "operation": None,  # string - The type of operation
        "region": None,  # string - Region
        "status": None,  # string - Status
        "log_url": None,  # string - Link to download the log file for this migration.
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
        ) in FileMigration.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in FileMigration.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
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
    return ListObj(FileMigration, "GET", "/file_migrations", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - File Migration ID.
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
        "/file_migrations/{id}".format(id=quote(str(params["id"]), safe="")),
        params,
        options,
    )
    return FileMigration(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    response, options = Api.send_request(
        "POST", "/file_migrations/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return FileMigration(*args, **kwargs)

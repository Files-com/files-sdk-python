import builtins  # noqa: F401
from files_sdk.models.action import Action
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class History:
    default_attributes = {
        "id": None,  # int64 - Action ID
        "path": None,  # string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "when": None,  # date-time - Action occurrence date/time
        "destination": None,  # string - The destination path for this action, if applicable
        "display": None,  # string - Friendly displayed output
        "ip": None,  # string - IP Address that performed this action
        "source": None,  # string - The source path for this action, if applicable
        "targets": None,  # array(object) - Targets
        "user_id": None,  # int64 - User ID
        "username": None,  # string - Username
        "user_is_from_parent_site": None,  # boolean - true if this change was performed by a user on a parent site.
        "action": None,  # string - Type of action
        "failure_type": None,  # string - Failure type.  If action was a user login or session failure, why did it fail?
        "interface": None,  # string - Interface on which this action occurred.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in History.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in History.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   start_at - string - Leave blank or set to a date/time to filter earlier entries.
#   end_at - string - Leave blank or set to a date/time to filter later entries.
#   display - string - Display format. Leave blank or set to `full` or `parent`.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `path` and `created_at`.
#   path (required) - string - Path to operate on.
def list_for_file(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "start_at" in params and not isinstance(params["start_at"], str):
        raise InvalidParameterError("Bad parameter: start_at must be an str")
    if "end_at" in params and not isinstance(params["end_at"], str):
        raise InvalidParameterError("Bad parameter: end_at must be an str")
    if "display" in params and not isinstance(params["display"], str):
        raise InvalidParameterError("Bad parameter: display must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(
        Action,
        "GET",
        "/history/files/{path}".format(path=params["path"]),
        params,
        options,
    )


# Parameters:
#   start_at - string - Leave blank or set to a date/time to filter earlier entries.
#   end_at - string - Leave blank or set to a date/time to filter later entries.
#   display - string - Display format. Leave blank or set to `full` or `parent`.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
#   path (required) - string - Path to operate on.
def list_for_folder(path, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "start_at" in params and not isinstance(params["start_at"], str):
        raise InvalidParameterError("Bad parameter: start_at must be an str")
    if "end_at" in params and not isinstance(params["end_at"], str):
        raise InvalidParameterError("Bad parameter: end_at must be an str")
    if "display" in params and not isinstance(params["display"], str):
        raise InvalidParameterError("Bad parameter: display must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(
        Action,
        "GET",
        "/history/folders/{path}".format(path=params["path"]),
        params,
        options,
    )


# Parameters:
#   start_at - string - Leave blank or set to a date/time to filter earlier entries.
#   end_at - string - Leave blank or set to a date/time to filter later entries.
#   display - string - Display format. Leave blank or set to `full` or `parent`.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `user_id` and `created_at`.
#   user_id (required) - int64 - User ID.
def list_for_user(user_id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["user_id"] = user_id
    if "start_at" in params and not isinstance(params["start_at"], str):
        raise InvalidParameterError("Bad parameter: start_at must be an str")
    if "end_at" in params and not isinstance(params["end_at"], str):
        raise InvalidParameterError("Bad parameter: end_at must be an str")
    if "display" in params and not isinstance(params["display"], str):
        raise InvalidParameterError("Bad parameter: display must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "user_id" not in params:
        raise MissingParameterError("Parameter missing: user_id")
    return ListObj(
        Action,
        "GET",
        "/history/users/{user_id}".format(user_id=params["user_id"]),
        params,
        options,
    )


# Parameters:
#   start_at - string - Leave blank or set to a date/time to filter earlier entries.
#   end_at - string - Leave blank or set to a date/time to filter later entries.
#   display - string - Display format. Leave blank or set to `full` or `parent`.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`.
def list_logins(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "start_at" in params and not isinstance(params["start_at"], str):
        raise InvalidParameterError("Bad parameter: start_at must be an str")
    if "end_at" in params and not isinstance(params["end_at"], str):
        raise InvalidParameterError("Bad parameter: end_at must be an str")
    if "display" in params and not isinstance(params["display"], str):
        raise InvalidParameterError("Bad parameter: display must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    return ListObj(Action, "GET", "/history/login", params, options)


# Parameters:
#   start_at - string - Leave blank or set to a date/time to filter earlier entries.
#   end_at - string - Leave blank or set to a date/time to filter later entries.
#   display - string - Display format. Leave blank or set to `full` or `parent`.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `path`, `created_at` or `user_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `user_id`, `folder` or `path`. Valid field combinations are `[ user_id, folder ]`, `[ user_id, path ]`, `[ folder, path ]` or `[ user_id, folder, path ]`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "start_at" in params and not isinstance(params["start_at"], str):
        raise InvalidParameterError("Bad parameter: start_at must be an str")
    if "end_at" in params and not isinstance(params["end_at"], str):
        raise InvalidParameterError("Bad parameter: end_at must be an str")
    if "display" in params and not isinstance(params["display"], str):
        raise InvalidParameterError("Bad parameter: display must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    return ListObj(Action, "GET", "/history", params, options)


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return History(*args, **kwargs)

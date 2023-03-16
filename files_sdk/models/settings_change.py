import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class SettingsChange:
    default_attributes = {
        'changes': None,     # array - Markdown-formatted change messages.
        'created_at': None,     # date-time - The time this change was made
        'user_id': None,     # int64 - The user id responsible for this change
        'user_is_files_support': None,     # boolean - true if this change was performed by Files.com support.
        'username': None,     # string - The username of the user responsible for this change
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in SettingsChange.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in SettingsChange.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[api_key_id]=desc`). Valid fields are `api_key_id`, `created_at` or `user_id`.
#   api_key_id - string - If set, return records where the specified field is equal to the supplied value.
#   user_id - string - If set, return records where the specified field is equal to the supplied value.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `api_key_id` and `user_id`.
def list(params = None, options = None):
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
    if "api_key_id" in params and not isinstance(params["api_key_id"], str):
        raise InvalidParameterError("Bad parameter: api_key_id must be an str")
    if "user_id" in params and not isinstance(params["user_id"], str):
        raise InvalidParameterError("Bad parameter: user_id must be an str")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    return ListObj(SettingsChange,"GET", "/settings_changes", params, options)

def all(params = None, options = None):
    list(params, options)

def new(*args, **kwargs):
    return SettingsChange(*args, **kwargs)
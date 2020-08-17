import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class UsageSnapshot:
    default_attributes = {
        'id': None,     # int64 - Site usage ID
        'start_at': None,     # date-time - Site usage report start date/time
        'end_at': None,     # date-time - Site usage report end date/time
        'created_at': None,     # date-time - Site usage report created at date/time
        'current_storage': None,     # double - Current site usage as of report
        'high_water_storage': None,     # double - Site usage report highest usage in time period
        'total_downloads': None,     # int64 - Number of downloads in report time period
        'total_uploads': None,     # int64 - Number of uploads in time period
        'updated_at': None,     # date-time - The last time this site usage report was updated
        'usage_by_top_level_dir': None,     # object - A map of root folders to their total usage
        'root_storage': None,     # double - Usage for root folder
        'deleted_files_counted_in_minimum': None,     # double - Usage for files that are deleted but uploaded within last 30 days
        'deleted_files_storage': None,     # double - Usage for files that are deleted but retained as backups
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in UsageSnapshot.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in UsageSnapshot.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   page - int64 - Current page number.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
def list(params = {}, options = {}):
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    return ListObj(UsageSnapshot,"GET", "/usage_snapshots", params, options)

def all(params = {}, options = {}):
    list(params, options)

def new(*args, **kwargs):
    return UsageSnapshot(*args, **kwargs)
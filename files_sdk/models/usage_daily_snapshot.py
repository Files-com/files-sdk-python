import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class UsageDailySnapshot:
    default_attributes = {
        "id": None,  # int64 - ID of the usage record
        "date": None,  # date - The date of this usage record
        "api_usage_available": None,  # boolean - True if the API usage fields `read_api_usage` and `write_api_usage` can be relied upon.  If this is false, we suggest hiding that value from any UI.
        "read_api_usage": None,  # int64 - Read API Calls used on this day. Note: only updated for days before the current day.
        "write_api_usage": None,  # int64 - Write API Calls used on this day. Note: only updated for days before the current day.
        "user_count": None,  # int64 - Number of billable users as of this day.
        "current_storage": None,  # double - GB of Files Native Storage used on this day.
        "deleted_files_storage": None,  # double - GB of Files Native Storage used on this day for files that have been deleted and are stored as backups.
        "deleted_files_counted_in_minimum": None,  # double - GB of Files Native Storage used on this day for files that have been permanently deleted but were uploaded less than 30 days ago, and are still billable.
        "root_storage": None,  # double - GB of Files Native Storage used for the root folder.  Included here because this value will not be part of `usage_by_top_level_dir`
        "usage_by_top_level_dir": None,  # array(object) - Usage broken down by each top-level folder
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
        ) in UsageDailySnapshot.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in UsageDailySnapshot.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `date`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `date`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `date`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `date`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `date`.
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
    return ListObj(
        UsageDailySnapshot, "GET", "/usage_daily_snapshots", params, options
    )


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return UsageDailySnapshot(*args, **kwargs)

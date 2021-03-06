import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class UsageDailySnapshot:
    default_attributes = {
        'id': None,     # int64 - ID of the usage record
        'date': None,     # date - The date of this usage record
        'current_storage': None,     # int64 - The quantity of storage held for this site
        'usage_by_top_level_dir': None,     # array - Usage broken down by each top-level folder
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in UsageDailySnapshot.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in UsageDailySnapshot.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `date` and `usage_snapshot_id`.
#   filter - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`.
#   filter_gt - object - If set, return records where the specifiied field is greater than the supplied value. Valid fields are `date` and `usage_snapshot_id`.
#   filter_gteq - object - If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`.
#   filter_like - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`.
#   filter_lt - object - If set, return records where the specifiied field is less than the supplied value. Valid fields are `date` and `usage_snapshot_id`.
#   filter_lteq - object - If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`.
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
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
        raise InvalidParameterError("Bad parameter: filter_gt must be an dict")
    if "filter_gteq" in params and not isinstance(params["filter_gteq"], dict):
        raise InvalidParameterError("Bad parameter: filter_gteq must be an dict")
    if "filter_like" in params and not isinstance(params["filter_like"], dict):
        raise InvalidParameterError("Bad parameter: filter_like must be an dict")
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError("Bad parameter: filter_lteq must be an dict")
    return ListObj(UsageDailySnapshot,"GET", "/usage_daily_snapshots", params, options)

def all(params = None, options = None):
    list(params, options)

def new(*args, **kwargs):
    return UsageDailySnapshot(*args, **kwargs)
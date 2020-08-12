import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class BandwidthSnapshot:
    default_attributes = {
        'id': None,     # int64 - Site bandwidth ID
        'bytes_received': None,     # double - Site bandwidth report bytes received
        'bytes_sent': None,     # double - Site bandwidth report bytes sent
        'requests_get': None,     # double - Site bandwidth report get requests
        'requests_put': None,     # double - Site bandwidth report put requests
        'requests_other': None,     # double - Site bandwidth report other requests
        'logged_at': None,     # date-time - Time the site bandwidth report was logged
        'created_at': None,     # date-time - Site bandwidth report created at date/time
        'updated_at': None,     # date-time - The last time this site bandwidth report was updated
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in BandwidthSnapshot.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in BandwidthSnapshot.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   page - int64 - Current page number.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `site_id` and `logged_at`.
#   filter - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `logged_at`.
#   filter_gt - object - If set, return records where the specifiied field is greater than the supplied value. Valid fields are `logged_at`.
#   filter_gteq - object - If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `logged_at`.
#   filter_like - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `logged_at`.
#   filter_lt - object - If set, return records where the specifiied field is less than the supplied value. Valid fields are `logged_at`.
#   filter_lteq - object - If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `logged_at`.
def list(params = {}, options = {}):
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
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
    return ListObj(BandwidthSnapshot,"GET", "/bandwidth_snapshots", params, options)

def all(params = {}, options = {}):
    list(params, options)

def new(*args, **kwargs):
    return BandwidthSnapshot(*args, **kwargs)
import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class RemoteBandwidthSnapshot:
    default_attributes = {
        "id": None,  # int64 - Site bandwidth ID
        "sync_bytes_received": None,  # double - Site sync bandwidth report bytes received
        "sync_bytes_sent": None,  # double - Site sync bandwidth report bytes sent
        "logged_at": None,  # date-time - Time the site bandwidth report was logged
        "remote_server_id": None,  # int64 - ID of related Remote Server
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
        ) in RemoteBandwidthSnapshot.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in RemoteBandwidthSnapshot.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[logged_at]=desc`). Valid fields are `logged_at`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `logged_at`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `logged_at`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `logged_at`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `logged_at`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `logged_at`.
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
        RemoteBandwidthSnapshot,
        "GET",
        "/remote_bandwidth_snapshots",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return RemoteBandwidthSnapshot(*args, **kwargs)

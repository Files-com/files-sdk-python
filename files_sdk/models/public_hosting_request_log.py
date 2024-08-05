import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class PublicHostingRequestLog:
    default_attributes = {
        "timestamp": None,  # date-time - Start Time of Action
        "remote_ip": None,  # string - IP Address of Public Hosting Client
        "server_ip": None,  # string - IP Address of Public Hosting Server
        "hostname": None,  # string - HTTP Request Hostname
        "path": None,  # string - HTTP Request Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "responseCode": None,  # int64 - HTTP Response Code
        "success": None,  # boolean - Whether SFTP Action was successful.
        "duration_ms": None,  # int64 - Duration (in milliseconds)
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
        ) in PublicHostingRequestLog.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in PublicHostingRequestLog.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `start_date`, `end_date`, `path`, `remote_ip` or `success`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ path ]`, `[ remote_ip ]`, `[ success ]`, `[ start_date, end_date ]`, `[ start_date, path ]`, `[ start_date, remote_ip ]`, `[ start_date, success ]`, `[ end_date, path ]`, `[ end_date, remote_ip ]`, `[ end_date, success ]`, `[ path, remote_ip ]`, `[ path, success ]`, `[ remote_ip, success ]`, `[ start_date, end_date, path ]`, `[ start_date, end_date, remote_ip ]`, `[ start_date, end_date, success ]`, `[ start_date, path, remote_ip ]`, `[ start_date, path, success ]`, `[ start_date, remote_ip, success ]`, `[ end_date, path, remote_ip ]`, `[ end_date, path, success ]`, `[ end_date, remote_ip, success ]`, `[ path, remote_ip, success ]`, `[ start_date, end_date, path, remote_ip ]`, `[ start_date, end_date, path, success ]`, `[ start_date, end_date, remote_ip, success ]`, `[ start_date, path, remote_ip, success ]` or `[ end_date, path, remote_ip, success ]`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ path ]`, `[ remote_ip ]`, `[ success ]`, `[ start_date, end_date ]`, `[ start_date, path ]`, `[ start_date, remote_ip ]`, `[ start_date, success ]`, `[ end_date, path ]`, `[ end_date, remote_ip ]`, `[ end_date, success ]`, `[ path, remote_ip ]`, `[ path, success ]`, `[ remote_ip, success ]`, `[ start_date, end_date, path ]`, `[ start_date, end_date, remote_ip ]`, `[ start_date, end_date, success ]`, `[ start_date, path, remote_ip ]`, `[ start_date, path, success ]`, `[ start_date, remote_ip, success ]`, `[ end_date, path, remote_ip ]`, `[ end_date, path, success ]`, `[ end_date, remote_ip, success ]`, `[ path, remote_ip, success ]`, `[ start_date, end_date, path, remote_ip ]`, `[ start_date, end_date, path, success ]`, `[ start_date, end_date, remote_ip, success ]`, `[ start_date, path, remote_ip, success ]` or `[ end_date, path, remote_ip, success ]`.
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
        PublicHostingRequestLog,
        "GET",
        "/public_hosting_request_logs",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return PublicHostingRequestLog(*args, **kwargs)

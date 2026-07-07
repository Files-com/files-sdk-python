import builtins  # noqa: F401
from files_sdk.models.export import Export
from files_sdk.api import Api  # noqa: F401
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class IpAbuseEntry:
    default_attributes = {
        "ip": None,  # string
        "list": None,  # string
        "hostname": None,  # string
        "reason": None,  # string
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
        ) in IpAbuseEntry.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in IpAbuseEntry.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The IpAbuseEntry object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    Api.send_request("GET", "/ip_abuse_entries", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   ip (required) - string
#   list - string
#   hostname - string
#   reason - string
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "ip" in params and not isinstance(params["ip"], str):
        raise InvalidParameterError("Bad parameter: ip must be an str")
    if "list" in params and not isinstance(params["list"], str):
        raise InvalidParameterError("Bad parameter: list must be an str")
    if "hostname" in params and not isinstance(params["hostname"], str):
        raise InvalidParameterError("Bad parameter: hostname must be an str")
    if "reason" in params and not isinstance(params["reason"], str):
        raise InvalidParameterError("Bad parameter: reason must be an str")
    if "ip" not in params:
        raise MissingParameterError("Parameter missing: ip")
    Api.send_request("POST", "/ip_abuse_entries", params, options)


def create_export(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    response, options = Api.send_request(
        "POST", "/ip_abuse_entries/create_export", params, options
    )
    return Export(response.data, options)


def new(*args, **kwargs):
    return IpAbuseEntry(*args, **kwargs)

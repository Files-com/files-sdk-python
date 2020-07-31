import datetime
from files_sdk.api import Api
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
def list(params = {}, options = {}):
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    response, options = Api.send_request("GET", "/bandwidth_snapshots", params, options)
    return [ BandwidthSnapshot(entity_data, options) for entity_data in response.data ]

def all(params = {}, options = {}):
    list(params, options)

def new(*args, **kwargs):
    return BandwidthSnapshot(*args, **kwargs)
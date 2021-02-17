import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class InboxUpload:
    default_attributes = {
        'inbox_registration': None,         'path': None,     # string - Upload path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'created_at': None,     # date-time - Upload date/time
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in InboxUpload.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in InboxUpload.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   inbox_registration_id - int64 - InboxRegistration ID
#   inbox_id - int64 - Inbox ID
def list(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "inbox_registration_id" in params and not isinstance(params["inbox_registration_id"], int):
        raise InvalidParameterError("Bad parameter: inbox_registration_id must be an int")
    if "inbox_id" in params and not isinstance(params["inbox_id"], int):
        raise InvalidParameterError("Bad parameter: inbox_id must be an int")
    return ListObj(InboxUpload,"GET", "/inbox_uploads", params, options)

def all(params = None, options = None):
    list(params, options)

def new(*args, **kwargs):
    return InboxUpload(*args, **kwargs)
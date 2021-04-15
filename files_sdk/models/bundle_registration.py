import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class BundleRegistration:
    default_attributes = {
        'code': None,     # string - Registration cookie code
        'name': None,     # string - Registrant name
        'company': None,     # string - Registrant company name
        'email': None,     # string - Registrant email address
        'inbox_code': None,     # string - InboxRegistration cookie code, if there is an associated InboxRegistration
        'clickwrap_body': None,     # string - Clickwrap text that was shown to the registrant
        'form_field_set_id': None,     # int64 - Id of associated form field set
        'form_field_data': None,     # string - Data for form field set with form field ids as keys and user data as values
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in BundleRegistration.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in BundleRegistration.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   bundle_id (required) - int64 - ID of the associated Bundle
def list(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "bundle_id" in params and not isinstance(params["bundle_id"], int):
        raise InvalidParameterError("Bad parameter: bundle_id must be an int")
    if "bundle_id" not in params:
        raise MissingParameterError("Parameter missing: bundle_id")
    return ListObj(BundleRegistration,"GET", "/bundle_registrations", params, options)

def all(params = None, options = None):
    list(params, options)

def new(*args, **kwargs):
    return BundleRegistration(*args, **kwargs)
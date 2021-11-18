import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class BundleRecipient:
    default_attributes = {
        'company': None,     # string - The recipient's company.
        'name': None,     # string - The recipient's name.
        'note': None,     # string - A note sent to the recipient with the bundle.
        'recipient': None,     # string - The recipient's email address.
        'sent_at': None,     # date-time - When the Bundle was shared with this recipient.
        'user_id': None,     # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        'bundle_id': None,     # int64 - Bundle to share.
        'share_after_create': None,     # boolean - Set to true to share the link with the recipient upon creation.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in BundleRecipient.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in BundleRecipient.default_attributes if getattr(self, k, None) is not None}

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The BundleRecipient object doesn't support updates.")
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `has_registrations`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `has_registrations`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `has_registrations`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `has_registrations`.
#   filter_like - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `has_registrations`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `has_registrations`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `has_registrations`.
#   bundle_id (required) - int64 - List recipients for the bundle with this ID.
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
    if "bundle_id" in params and not isinstance(params["bundle_id"], int):
        raise InvalidParameterError("Bad parameter: bundle_id must be an int")
    if "bundle_id" not in params:
        raise MissingParameterError("Parameter missing: bundle_id")
    return ListObj(BundleRecipient,"GET", "/bundle_recipients", params, options)

def all(params = None, options = None):
    list(params, options)

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   bundle_id (required) - int64 - Bundle to share.
#   recipient (required) - string - Email addresses to share this bundle with.
#   name - string - Name of recipient.
#   company - string - Company of recipient.
#   note - string - Note to include in email.
#   share_after_create - boolean - Set to true to share the link with the recipient upon creation.
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "bundle_id" in params and not isinstance(params["bundle_id"], int):
        raise InvalidParameterError("Bad parameter: bundle_id must be an int")
    if "recipient" in params and not isinstance(params["recipient"], str):
        raise InvalidParameterError("Bad parameter: recipient must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "company" in params and not isinstance(params["company"], str):
        raise InvalidParameterError("Bad parameter: company must be an str")
    if "note" in params and not isinstance(params["note"], str):
        raise InvalidParameterError("Bad parameter: note must be an str")
    if "bundle_id" not in params:
        raise MissingParameterError("Parameter missing: bundle_id")
    if "recipient" not in params:
        raise MissingParameterError("Parameter missing: recipient")
    response, options = Api.send_request("POST", "/bundle_recipients", params, options)
    return BundleRecipient(response.data, options)

def new(*args, **kwargs):
    return BundleRecipient(*args, **kwargs)
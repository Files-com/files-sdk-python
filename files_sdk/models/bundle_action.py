import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class BundleAction:
    default_attributes = {
        "action": None,  # string - Type of action
        "bundle_registration": None,  # BundleRegistration - Object that contains bundle registration information
        "created_at": None,  # date-time - Action occurrence date/time
        "destination": None,  # string - The destination path for this bundle action, if applicable
        "path": None,  # string - Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "source": None,  # string - The source path for this bundle action, if applicable
        "bundle_registration_id": None,  # int64 - Identifier of the associated bundle registration
        "bundle_registration_name": None,  # string - Name of the registrant who performed the action
        "bundle_registration_email": None,  # string - Email of the registrant
        "bundle_registration_ip": None,  # string - IP address of the registrant
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
        ) in BundleAction.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in BundleAction.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at` and `bundle_registration_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `bundle_id` or `bundle_registration_id`. Valid field combinations are `[ bundle_id, created_at ]`, `[ bundle_registration_id, created_at ]`, `[ bundle_id, bundle_registration_id ]` or `[ bundle_id, bundle_registration_id, created_at ]`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
def list(params=None, options=None):
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
        raise InvalidParameterError(
            "Bad parameter: filter_gteq must be an dict"
        )
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_lteq must be an dict"
        )
    return ListObj(BundleAction, "GET", "/bundle_actions", params, options)


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return BundleAction(*args, **kwargs)

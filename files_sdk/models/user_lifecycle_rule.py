import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class UserLifecycleRule:
    default_attributes = {
        "id": None,  # int64 - User Lifecycle Rule ID
        "authentication_method": None,  # string - User authentication method for the rule
        "inactivity_days": None,  # int64 - Number of days of inactivity before the rule applies
        "include_folder_admins": None,  # boolean - Include folder admins in the rule
        "include_site_admins": None,  # boolean - Include site admins in the rule
        "action": None,  # string - Action to take on inactive users (disable or delete)
        "site_id": None,  # int64 - Site ID
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
        ) in UserLifecycleRule.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in UserLifecycleRule.default_attributes
            if getattr(self, k, None) is not None
        }

    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "DELETE",
            "/user_lifecycle_rules/{id}".format(id=params["id"]),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The UserLifecycleRule object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(
        UserLifecycleRule, "GET", "/user_lifecycle_rules", params, options
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - User Lifecycle Rule ID.
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET",
        "/user_lifecycle_rules/{id}".format(id=params["id"]),
        params,
        options,
    )
    return UserLifecycleRule(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   action (required) - string - Action to take on inactive users (disable or delete)
#   authentication_method (required) - string - User authentication method for the rule
#   inactivity_days (required) - int64 - Number of days of inactivity before the rule applies
#   include_site_admins - boolean - Include site admins in the rule
#   include_folder_admins - boolean - Include folder admins in the rule
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "authentication_method" in params and not isinstance(
        params["authentication_method"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: authentication_method must be an str"
        )
    if "inactivity_days" in params and not isinstance(
        params["inactivity_days"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: inactivity_days must be an int"
        )
    if "include_site_admins" in params and not isinstance(
        params["include_site_admins"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: include_site_admins must be an bool"
        )
    if "include_folder_admins" in params and not isinstance(
        params["include_folder_admins"], bool
    ):
        raise InvalidParameterError(
            "Bad parameter: include_folder_admins must be an bool"
        )
    if "action" not in params:
        raise MissingParameterError("Parameter missing: action")
    if "authentication_method" not in params:
        raise MissingParameterError("Parameter missing: authentication_method")
    if "inactivity_days" not in params:
        raise MissingParameterError("Parameter missing: inactivity_days")
    response, options = Api.send_request(
        "POST", "/user_lifecycle_rules", params, options
    )
    return UserLifecycleRule(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "DELETE",
        "/user_lifecycle_rules/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return UserLifecycleRule(*args, **kwargs)

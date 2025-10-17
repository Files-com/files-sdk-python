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
        "authentication_method": None,  # string - User authentication method for which the rule will apply.
        "group_ids": None,  # array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
        "action": None,  # string - Action to take on inactive users (disable or delete)
        "inactivity_days": None,  # int64 - Number of days of inactivity before the rule applies
        "include_folder_admins": None,  # boolean - If true, the rule will apply to folder admins.
        "include_site_admins": None,  # boolean - If true, the rule will apply to site admins.
        "name": None,  # string - User Lifecycle Rule name
        "partner_tag": None,  # string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
        "site_id": None,  # int64 - Site ID
        "user_state": None,  # string - State of the users to apply the rule to (inactive or disabled)
        "user_tag": None,  # string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
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

    # Parameters:
    #   action - string - Action to take on inactive users (disable or delete)
    #   authentication_method - string - User authentication method for which the rule will apply.
    #   group_ids - array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
    #   inactivity_days - int64 - Number of days of inactivity before the rule applies
    #   include_site_admins - boolean - If true, the rule will apply to site admins.
    #   include_folder_admins - boolean - If true, the rule will apply to folder admins.
    #   name - string - User Lifecycle Rule name
    #   partner_tag - string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
    #   user_state - string - State of the users to apply the rule to (inactive or disabled)
    #   user_tag - string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
    def update(self, params=None):
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
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "authentication_method" in params and not isinstance(
            params["authentication_method"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: authentication_method must be an str"
            )
        if "group_ids" in params and not isinstance(
            params["group_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an list"
            )
        if "inactivity_days" in params and not isinstance(
            params["inactivity_days"], int
        ):
            raise InvalidParameterError(
                "Bad parameter: inactivity_days must be an int"
            )
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "partner_tag" in params and not isinstance(
            params["partner_tag"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: partner_tag must be an str"
            )
        if "user_state" in params and not isinstance(
            params["user_state"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: user_state must be an str"
            )
        if "user_tag" in params and not isinstance(params["user_tag"], str):
            raise InvalidParameterError(
                "Bad parameter: user_tag must be an str"
            )
        response, _options = Api.send_request(
            "PATCH",
            "/user_lifecycle_rules/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

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
            new_obj = self.update(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            return True
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`.
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
#   action - string - Action to take on inactive users (disable or delete)
#   authentication_method - string - User authentication method for which the rule will apply.
#   group_ids - array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
#   inactivity_days - int64 - Number of days of inactivity before the rule applies
#   include_site_admins - boolean - If true, the rule will apply to site admins.
#   include_folder_admins - boolean - If true, the rule will apply to folder admins.
#   name - string - User Lifecycle Rule name
#   partner_tag - string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
#   user_state - string - State of the users to apply the rule to (inactive or disabled)
#   user_tag - string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
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
    if "group_ids" in params and not isinstance(
        params["group_ids"], builtins.list
    ):
        raise InvalidParameterError("Bad parameter: group_ids must be an list")
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
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "partner_tag" in params and not isinstance(params["partner_tag"], str):
        raise InvalidParameterError(
            "Bad parameter: partner_tag must be an str"
        )
    if "user_state" in params and not isinstance(params["user_state"], str):
        raise InvalidParameterError("Bad parameter: user_state must be an str")
    if "user_tag" in params and not isinstance(params["user_tag"], str):
        raise InvalidParameterError("Bad parameter: user_tag must be an str")
    response, options = Api.send_request(
        "POST", "/user_lifecycle_rules", params, options
    )
    return UserLifecycleRule(response.data, options)


# Parameters:
#   action - string - Action to take on inactive users (disable or delete)
#   authentication_method - string - User authentication method for which the rule will apply.
#   group_ids - array(int64) - Array of Group IDs to which the rule applies. If empty or not set, the rule applies to all users.
#   inactivity_days - int64 - Number of days of inactivity before the rule applies
#   include_site_admins - boolean - If true, the rule will apply to site admins.
#   include_folder_admins - boolean - If true, the rule will apply to folder admins.
#   name - string - User Lifecycle Rule name
#   partner_tag - string - If provided, only users belonging to Partners with this tag at the Partner level will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
#   user_state - string - State of the users to apply the rule to (inactive or disabled)
#   user_tag - string - If provided, only users with this tag will be affected by the rule. Tags must only contain lowercase letters, numbers, and hyphens.
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "authentication_method" in params and not isinstance(
        params["authentication_method"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: authentication_method must be an str"
        )
    if "group_ids" in params and not isinstance(
        params["group_ids"], builtins.list
    ):
        raise InvalidParameterError("Bad parameter: group_ids must be an list")
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
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "partner_tag" in params and not isinstance(params["partner_tag"], str):
        raise InvalidParameterError(
            "Bad parameter: partner_tag must be an str"
        )
    if "user_state" in params and not isinstance(params["user_state"], str):
        raise InvalidParameterError("Bad parameter: user_state must be an str")
    if "user_tag" in params and not isinstance(params["user_tag"], str):
        raise InvalidParameterError("Bad parameter: user_tag must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH",
        "/user_lifecycle_rules/{id}".format(id=params["id"]),
        params,
        options,
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

import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Permission:
    default_attributes = {
        "id": None,  # int64 - Permission ID
        "path": None,  # string - Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "user_id": None,  # int64 - User ID
        "username": None,  # string - User's username
        "group_id": None,  # int64 - Group ID
        "group_name": None,  # string - Group name if applicable
        "permission": None,  # string - Permission type
        "recursive": None,  # boolean - Does this permission apply to subfolders?
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Permission.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Permission.default_attributes
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
            "/permissions/{id}".format(id=params["id"]),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The Permission object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[group_id]=desc`). Valid fields are `group_id`, `path`, `user_id` or `permission`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `group_id` or `user_id`. Valid field combinations are `[ group_id, path ]`, `[ user_id, path ]` or `[ user_id, group_id, path ]`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
#   path - string - Permission path.  If provided, will scope all permissions(including upward) to this path.
#   include_groups - boolean - If searching by user or group, also include user's permissions that are inherited from its groups?
#   group_id - string
#   user_id - string
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
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "group_id" in params and not isinstance(params["group_id"], str):
        raise InvalidParameterError("Bad parameter: group_id must be an str")
    if "user_id" in params and not isinstance(params["user_id"], str):
        raise InvalidParameterError("Bad parameter: user_id must be an str")
    return ListObj(Permission, "GET", "/permissions", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   group_id - int64 - Group ID
#   path - string - Folder path
#   permission - string -  Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`
#   recursive - boolean - Apply to subfolders recursively?
#   user_id - int64 - User ID.  Provide `username` or `user_id`
#   username - string - User username.  Provide `username` or `user_id`
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "group_id" in params and not isinstance(params["group_id"], int):
        raise InvalidParameterError("Bad parameter: group_id must be an int")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "permission" in params and not isinstance(params["permission"], str):
        raise InvalidParameterError("Bad parameter: permission must be an str")
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    response, options = Api.send_request(
        "POST", "/permissions", params, options
    )
    return Permission(response.data, options)


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
        "DELETE", "/permissions/{id}".format(id=params["id"]), params, options
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Permission(*args, **kwargs)

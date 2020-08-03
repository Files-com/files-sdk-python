import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Permission:
    default_attributes = {
        'id': None,     # int64 - Permission ID
        'path': None,     # string - Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'user_id': None,     # int64 - User ID
        'username': None,     # string - User's username
        'group_id': None,     # int64 - Group ID
        'group_name': None,     # string - Group name if applicable
        'permission': None,     # string - Permission type
        'recursive': None,     # boolean - Does this permission apply to subfolders?
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Permission.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Permission.default_attributes if getattr(self, k, None) is not None}

    def delete(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        response, _options = Api.send_request("DELETE", "/permissions/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The Permission object doesn't support updates.")
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   page - int64 - Current page number.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `deleted_at`, `group_id`, `path`, `user_id` or `permission`.
#   filter - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `group_id`, `user_id` or `path`.
#   filter_gt - object - If set, return records where the specifiied field is greater than the supplied value. Valid fields are `group_id`, `user_id` or `path`.
#   filter_gteq - object - If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `group_id`, `user_id` or `path`.
#   filter_like - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `group_id`, `user_id` or `path`.
#   filter_lt - object - If set, return records where the specifiied field is less than the supplied value. Valid fields are `group_id`, `user_id` or `path`.
#   filter_lteq - object - If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `group_id`, `user_id` or `path`.
#   path - string - DEPRECATED: Permission path.  If provided, will scope permissions to this path. Use `filter[path]` instead.
#   group_id - string - DEPRECATED: Group ID.  If provided, will scope permissions to this group. Use `filter[group_id]` instead.`
#   user_id - string - DEPRECATED: User ID.  If provided, will scope permissions to this user. Use `filter[user_id]` instead.`
#   include_groups - boolean - If searching by user or group, also include user's permissions that are inherited from its groups?
def list(params = {}, options = {}):
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
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
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "group_id" in params and not isinstance(params["group_id"], str):
        raise InvalidParameterError("Bad parameter: group_id must be an str")
    if "user_id" in params and not isinstance(params["user_id"], str):
        raise InvalidParameterError("Bad parameter: user_id must be an str")
    return ListObj(Permission,"GET", "/permissions", params, options)

def all(params = {}, options = {}):
    list(params, options)

# Parameters:
#   group_id - int64 - Group ID
#   path - string - Folder path
#   permission - string -  Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`
#   recursive - boolean - Apply to subfolders recursively?
#   user_id - int64 - User ID.  Provide `username` or `user_id`
#   username - string - User username.  Provide `username` or `user_id`
def create(params = {}, options = {}):
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
    response, options = Api.send_request("POST", "/permissions", params, options)
    return Permission(response.data, options)

def delete(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/permissions/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = {}, options = {}):
    delete(id, params, options)

def new(*args, **kwargs):
    return Permission(*args, **kwargs)
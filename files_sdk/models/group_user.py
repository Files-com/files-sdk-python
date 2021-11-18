import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class GroupUser:
    default_attributes = {
        'group_name': None,     # string - Group name
        'group_id': None,     # int64 - Group ID
        'user_id': None,     # int64 - User ID
        'admin': None,     # boolean - Is this user an administrator of this group?
        'usernames': None,     # array - A list of usernames for users in this group
        'id': None,     # int64 - Group User ID.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in GroupUser.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in GroupUser.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   group_id (required) - int64 - Group ID to add user to.
    #   user_id (required) - int64 - User ID to add to group.
    #   admin - boolean - Is the user a group administrator?
    def update(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and not isinstance(params["group_id"], int):
            raise InvalidParameterError("Bad parameter: group_id must be an int")
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        response, _options = Api.send_request("PATCH", "/group_users/{id}".format(id=params['id']), params, self.options)
        return response.data

    # Parameters:
    #   group_id (required) - int64 - Group ID from which to remove user.
    #   user_id (required) - int64 - User ID to remove from group.
    def delete(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and not isinstance(params["group_id"], int):
            raise InvalidParameterError("Bad parameter: group_id must be an int")
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        response, _options = Api.send_request("DELETE", "/group_users/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   user_id - int64 - User ID.  If provided, will return group_users of this user.
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   group_id - int64 - Group ID.  If provided, will return group_users of this group.
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
    if "group_id" in params and not isinstance(params["group_id"], int):
        raise InvalidParameterError("Bad parameter: group_id must be an int")
    return ListObj(GroupUser,"GET", "/group_users", params, options)

def all(params = None, options = None):
    list(params, options)

# Parameters:
#   group_id (required) - int64 - Group ID to add user to.
#   user_id (required) - int64 - User ID to add to group.
#   admin - boolean - Is the user a group administrator?
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "group_id" in params and not isinstance(params["group_id"], int):
        raise InvalidParameterError("Bad parameter: group_id must be an int")
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "group_id" not in params:
        raise MissingParameterError("Parameter missing: group_id")
    if "user_id" not in params:
        raise MissingParameterError("Parameter missing: user_id")
    response, options = Api.send_request("POST", "/group_users", params, options)
    return GroupUser(response.data, options)

# Parameters:
#   group_id (required) - int64 - Group ID to add user to.
#   user_id (required) - int64 - User ID to add to group.
#   admin - boolean - Is the user a group administrator?
def update(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "group_id" in params and not isinstance(params["group_id"], int):
        raise InvalidParameterError("Bad parameter: group_id must be an int")
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "group_id" not in params:
        raise MissingParameterError("Parameter missing: group_id")
    if "user_id" not in params:
        raise MissingParameterError("Parameter missing: user_id")
    response, options = Api.send_request("PATCH", "/group_users/{id}".format(id=params['id']), params, options)
    return GroupUser(response.data, options)

# Parameters:
#   group_id (required) - int64 - Group ID from which to remove user.
#   user_id (required) - int64 - User ID to remove from group.
def delete(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "group_id" in params and not isinstance(params["group_id"], int):
        raise InvalidParameterError("Bad parameter: group_id must be an int")
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "group_id" not in params:
        raise MissingParameterError("Parameter missing: group_id")
    if "user_id" not in params:
        raise MissingParameterError("Parameter missing: user_id")
    response, _options = Api.send_request("DELETE", "/group_users/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = None, options = None):
    delete(id, params, options)

def new(*args, **kwargs):
    return GroupUser(*args, **kwargs)
import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Group:
    default_attributes = {
        'id': None,     # int64 - Group ID
        'name': None,     # string - Group name
        'admin_ids': None,     # string - Comma-delimited list of user IDs who are group administrators (separated by commas)
        'notes': None,     # string - Notes about this group
        'user_ids': None,     # string - Comma-delimited list of user IDs who belong to this group (separated by commas)
        'usernames': None,     # string - Comma-delimited list of usernames who belong to this group (separated by commas)
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Group.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Group.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   name - string - Group name.
    #   notes - string - Group notes.
    #   user_ids - string - A list of user ids. If sent as a string, should be comma-delimited.
    #   admin_ids - string - A list of group admin user ids. If sent as a string, should be comma-delimited.
    def update(self, params = None):
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
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "notes" in params and not isinstance(params["notes"], str):
            raise InvalidParameterError("Bad parameter: notes must be an str")
        if "user_ids" in params and not isinstance(params["user_ids"], str):
            raise InvalidParameterError("Bad parameter: user_ids must be an str")
        if "admin_ids" in params and not isinstance(params["admin_ids"], str):
            raise InvalidParameterError("Bad parameter: admin_ids must be an str")
        response, _options = Api.send_request("PATCH", "/groups/{id}".format(id=params['id']), params, self.options)
        return response.data

    def delete(self, params = None):
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
        response, _options = Api.send_request("DELETE", "/groups/{id}".format(id=params['id']), params, self.options)
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
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `name`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `name`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `name`.
#   filter_like - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `name`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `name`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `name`.
#   ids - string - Comma-separated list of group ids to include in results.
def list(params = None, options = None):
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
    if "ids" in params and not isinstance(params["ids"], str):
        raise InvalidParameterError("Bad parameter: ids must be an str")
    return ListObj(Group,"GET", "/groups", params, options)

def all(params = None, options = None):
    list(params, options)

# Parameters:
#   id (required) - int64 - Group ID.
def find(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("GET", "/groups/{id}".format(id=params['id']), params, options)
    return Group(response.data, options)

def get(id, params = None, options = None):
    find(id, params, options)

# Parameters:
#   name - string - Group name.
#   notes - string - Group notes.
#   user_ids - string - A list of user ids. If sent as a string, should be comma-delimited.
#   admin_ids - string - A list of group admin user ids. If sent as a string, should be comma-delimited.
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "notes" in params and not isinstance(params["notes"], str):
        raise InvalidParameterError("Bad parameter: notes must be an str")
    if "user_ids" in params and not isinstance(params["user_ids"], str):
        raise InvalidParameterError("Bad parameter: user_ids must be an str")
    if "admin_ids" in params and not isinstance(params["admin_ids"], str):
        raise InvalidParameterError("Bad parameter: admin_ids must be an str")
    response, options = Api.send_request("POST", "/groups", params, options)
    return Group(response.data, options)

# Parameters:
#   name - string - Group name.
#   notes - string - Group notes.
#   user_ids - string - A list of user ids. If sent as a string, should be comma-delimited.
#   admin_ids - string - A list of group admin user ids. If sent as a string, should be comma-delimited.
def update(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "notes" in params and not isinstance(params["notes"], str):
        raise InvalidParameterError("Bad parameter: notes must be an str")
    if "user_ids" in params and not isinstance(params["user_ids"], str):
        raise InvalidParameterError("Bad parameter: user_ids must be an str")
    if "admin_ids" in params and not isinstance(params["admin_ids"], str):
        raise InvalidParameterError("Bad parameter: admin_ids must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("PATCH", "/groups/{id}".format(id=params['id']), params, options)
    return Group(response.data, options)

def delete(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/groups/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = None, options = None):
    delete(id, params, options)

def new(*args, **kwargs):
    return Group(*args, **kwargs)
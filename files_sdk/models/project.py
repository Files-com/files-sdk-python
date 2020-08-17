import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Project:
    default_attributes = {
        'id': None,     # int64 - Project ID
        'global_access': None,     # string - Global access settings
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Project.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Project.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   global_access (required) - string - Global permissions.  Can be: `none`, `anyone_with_read`, `anyone_with_full`.
    def update(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "global_access" not in params:
            raise MissingParameterError("Parameter missing: global_access")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "global_access" in params and not isinstance(params["global_access"], str):
            raise InvalidParameterError("Bad parameter: global_access must be an str")
        response, _options = Api.send_request("PATCH", "/projects/{id}".format(id=params['id']), params, self.options)
        return response.data

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
        response, _options = Api.send_request("DELETE", "/projects/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   page - int64 - Current page number.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
def list(params = {}, options = {}):
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    return ListObj(Project,"GET", "/projects", params, options)

def all(params = {}, options = {}):
    list(params, options)

# Parameters:
#   id (required) - int64 - Project ID.
def find(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("GET", "/projects/{id}".format(id=params['id']), params, options)
    return Project(response.data, options)

def get(id, params = {}, options = {}):
    find(id, params, options)

# Parameters:
#   global_access (required) - string - Global permissions.  Can be: `none`, `anyone_with_read`, `anyone_with_full`.
def create(params = {}, options = {}):
    if "global_access" in params and not isinstance(params["global_access"], str):
        raise InvalidParameterError("Bad parameter: global_access must be an str")
    if "global_access" not in params:
        raise MissingParameterError("Parameter missing: global_access")
    response, options = Api.send_request("POST", "/projects", params, options)
    return Project(response.data, options)

# Parameters:
#   global_access (required) - string - Global permissions.  Can be: `none`, `anyone_with_read`, `anyone_with_full`.
def update(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "global_access" in params and not isinstance(params["global_access"], str):
        raise InvalidParameterError("Bad parameter: global_access must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "global_access" not in params:
        raise MissingParameterError("Parameter missing: global_access")
    response, options = Api.send_request("PATCH", "/projects/{id}".format(id=params['id']), params, options)
    return Project(response.data, options)

def delete(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/projects/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = {}, options = {}):
    delete(id, params, options)

def new(*args, **kwargs):
    return Project(*args, **kwargs)
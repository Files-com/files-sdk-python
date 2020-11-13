import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Lock:
    default_attributes = {
        'path': None,     # string - Path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'timeout': None,     # int64 - Lock timeout
        'depth': None,     # string - Lock depth (0 or infinity)
        'owner': None,     # string - Owner of lock.  This can be any arbitrary string.
        'scope': None,     # string - Lock scope(shared or exclusive)
        'token': None,     # string - Lock token.  Use to release lock.
        'type': None,     # string - Lock type
        'user_id': None,     # int64 - Lock creator user ID
        'username': None,     # string - Lock creator username
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Lock.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Lock.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   token (required) - string - Lock token
    def delete(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params['path'] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "token" not in params:
            raise MissingParameterError("Parameter missing: token")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "token" in params and not isinstance(params["token"], str):
            raise InvalidParameterError("Bad parameter: token must be an str")
        response, _options = Api.send_request("DELETE", "/locks/{path}".format(path=params['path']), params, self.options)
        return response.data

    def destroy(self, params = None):
        self.delete(params)

    def save(self):
        new_obj = create(self.path, self.get_attributes(), self.options)
        self.set_attributes(new_obj.get_attributes())

# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   path (required) - string - Path to operate on.
#   include_children - boolean - Include locks from children objects?
def list_for(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(Lock,"GET", "/locks/{path}".format(path=params['path']), params, options)

# Parameters:
#   path (required) - string - Path
#   timeout - int64 - Lock timeout length
def create(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "timeout" in params and not isinstance(params["timeout"], int):
        raise InvalidParameterError("Bad parameter: timeout must be an int")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request("POST", "/locks/{path}".format(path=params['path']), params, options)
    return Lock(response.data, options)

# Parameters:
#   token (required) - string - Lock token
def delete(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "token" in params and not isinstance(params["token"], str):
        raise InvalidParameterError("Bad parameter: token must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "token" not in params:
        raise MissingParameterError("Parameter missing: token")
    response, _options = Api.send_request("DELETE", "/locks/{path}".format(path=params['path']), params, options)
    return response.data

def destroy(path, params = None, options = None):
    delete(path, params, options)

def new(*args, **kwargs):
    return Lock(*args, **kwargs)
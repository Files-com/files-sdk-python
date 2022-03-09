import builtins
import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Style:
    default_attributes = {
        'id': None,     # int64 - Style ID
        'path': None,     # string - Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'logo': None,     # Image - Logo
        'thumbnail': None,     # Image - Logo thumbnail
        'file': None,     # file - Logo for custom branding.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Style.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Style.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   file (required) - file - Logo for custom branding.
    def update(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params['path'] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "file" not in params:
            raise MissingParameterError("Parameter missing: file")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        response, _options = Api.send_request("PATCH", "/styles/{path}".format(path=params['path']), params, self.options)
        return response.data

    def delete(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params['path'] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        response, _options = Api.send_request("DELETE", "/styles/{path}".format(path=params['path']), params, self.options)
        return response.data

    def destroy(self, params = None):
        self.delete(params)

    def save(self):
        self.update(self.get_attributes())

# Parameters:
#   path (required) - string - Style path.
def find(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request("GET", "/styles/{path}".format(path=params['path']), params, options)
    return Style(response.data, options)

def get(path, params = None, options = None):
    find(path, params, options)

# Parameters:
#   file (required) - file - Logo for custom branding.
def update(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "file" not in params:
        raise MissingParameterError("Parameter missing: file")
    response, options = Api.send_request("PATCH", "/styles/{path}".format(path=params['path']), params, options)
    return Style(response.data, options)

def delete(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, _options = Api.send_request("DELETE", "/styles/{path}".format(path=params['path']), params, options)
    return response.data

def destroy(path, params = None, options = None):
    delete(path, params, options)

def new(*args, **kwargs):
    return Style(*args, **kwargs)
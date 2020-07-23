import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Style:
    default_attributes = {
        'id': None,     # int64 - Style ID
        'path': None,     # string - Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'logo': None,     # Logo
        'thumbnail': None,     # Logo thumbnail
        'file': None,     # file - Logo for custom branding.
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Style.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Style.default_attributes}

    # Parameters:
    #   file (required) - file - Logo for custom branding.
    def update(self, params = {}):
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
        return Api.send_request("PATCH", "/styles/{path}".format(path=params['path']), params, self.options)

    def delete(self, params = {}):
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
        return Api.send_request("DELETE", "/styles/{path}".format(path=params['path']), params, self.options)

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        self.update(self.get_attributes())

    # Parameters:
    #   path (required) - string - Style path.
    @staticmethod
    def do_find(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")

        response, options = Api.send_request("GET", "/styles/{path}".format(path=params['path']), params, options)
        return Style(response.data, options)

    @staticmethod
    def do_get(path, params = {}):
        Style.do_find(path, params)
    
    # Parameters:
    #   file (required) - file - Logo for custom branding.
    @staticmethod
    def do_update(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "file" not in params:
            raise MissingParameterError("Parameter missing: file")

        response, options = Api.send_request("PATCH", "/styles/{path}".format(path=params['path']), params, options)
        return Style(response.data, options)
    
    @staticmethod
    def do_delete(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")

        response, _options = Api.send_request("DELETE", "/styles/{path}".format(path=params['path']), params, options)
        return response.data

    @staticmethod
    def do_destroy(path, params = {}):
        Style.do_delete(path, params)
    
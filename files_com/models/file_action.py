import datetime
from files_com.models.file_part_upload import FilePartUpload
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FileAction:
    default_attributes = {
        'path': None,
        'destination': None,
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FileAction.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FileAction.default_attributes}

    # Copy file/folder
    #
    # Parameters:
    #   destination (required) - string - Copy destination path.
    #   structure - boolean - Copy structure only?
    def copy(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params['path'] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(params["destination"], str):
            raise InvalidParameterError("Bad parameter: destination must be an str")
        return Api.send_request("POST", "/file_actions/copy/{path}".format(path=params['path']), params, self.options)

    # Move file/folder
    #
    # Parameters:
    #   destination (required) - string - Move destination path.
    def move(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "path") and self.path:
            params['path'] = self.path
        else:
            raise MissingParameterError("Current object doesn't have a path")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(params["destination"], str):
            raise InvalidParameterError("Bad parameter: destination must be an str")
        return Api.send_request("POST", "/file_actions/move/{path}".format(path=params['path']), params, self.options)

    # Begin file upload
    #
    # Parameters:
    #   mkdir_parents - boolean - Create parent directories if they do not exist?
    #   part - int64 - Part if uploading a part.
    #   parts - int64 - How many parts to fetch?
    #   ref - string -
    #   restart - int64 - File byte offset to restart from.
    #   with_rename - boolean - Allow file rename instead of overwrite?
    def begin_upload(self, params = {}):
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
        if "part" in params and not isinstance(params["part"], int):
            raise InvalidParameterError("Bad parameter: part must be an int")
        if "parts" in params and not isinstance(params["parts"], int):
            raise InvalidParameterError("Bad parameter: parts must be an int")
        if "ref" in params and not isinstance(params["ref"], str):
            raise InvalidParameterError("Bad parameter: ref must be an str")
        if "restart" in params and not isinstance(params["restart"], int):
            raise InvalidParameterError("Bad parameter: restart must be an int")
        return Api.send_request("POST", "/file_actions/begin_upload/{path}".format(path=params['path']), params, self.options)


    # Copy file/folder
    #
    # Parameters:
    #   destination (required) - string - Copy destination path.
    #   structure - boolean - Copy structure only?
    @staticmethod
    def do_copy(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(params["destination"], str):
            raise InvalidParameterError("Bad parameter: destination must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")

        response, _options = Api.send_request("POST", "/file_actions/copy/{path}".format(path=params['path']), params, options)
        return response.data
    
    # Move file/folder
    #
    # Parameters:
    #   destination (required) - string - Move destination path.
    @staticmethod
    def do_move(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "destination" in params and not isinstance(params["destination"], str):
            raise InvalidParameterError("Bad parameter: destination must be an str")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")
        if "destination" not in params:
            raise MissingParameterError("Parameter missing: destination")

        response, _options = Api.send_request("POST", "/file_actions/move/{path}".format(path=params['path']), params, options)
        return response.data
    
    # Begin file upload
    #
    # Parameters:
    #   mkdir_parents - boolean - Create parent directories if they do not exist?
    #   part - int64 - Part if uploading a part.
    #   parts - int64 - How many parts to fetch?
    #   ref - string -
    #   restart - int64 - File byte offset to restart from.
    #   with_rename - boolean - Allow file rename instead of overwrite?
    @staticmethod
    def do_begin_upload(path, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["path"] = path
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "part" in params and not isinstance(params["part"], int):
            raise InvalidParameterError("Bad parameter: part must be an int")
        if "parts" in params and not isinstance(params["parts"], int):
            raise InvalidParameterError("Bad parameter: parts must be an int")
        if "ref" in params and not isinstance(params["ref"], str):
            raise InvalidParameterError("Bad parameter: ref must be an str")
        if "restart" in params and not isinstance(params["restart"], int):
            raise InvalidParameterError("Bad parameter: restart must be an int")
        if "path" not in params:
            raise MissingParameterError("Parameter missing: path")

        response, options = Api.send_request("POST", "/file_actions/begin_upload/{path}".format(path=params['path']), params, options)
        return [ FilePartUpload(entity_data, options) for entity_data in response.data ]
    
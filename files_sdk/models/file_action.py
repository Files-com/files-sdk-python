import datetime
from files_sdk.models.file_upload_part import FileUploadPart
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FileAction:
    default_attributes = {
        'status': None,     # string - Status of file operation. Possible values: completed, enqueued.
        'file_migration_id': None,     # int64 - If status is enqueued, this is the id of the FileMigration to check for status updates.
        'path': None,
        'destination': None,
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FileAction.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FileAction.default_attributes if getattr(self, k, None) is not None}

    # Copy file/folder
    #
    # Parameters:
    #   destination (required) - string - Copy destination path.
    #   structure - boolean - Copy structure only?
    def copy(self, params = None):
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
        response, _options = Api.send_request("POST", "/file_actions/copy/{path}".format(path=params['path']), params, self.options)
        return response.data

    # Move file/folder
    #
    # Parameters:
    #   destination (required) - string - Move destination path.
    def move(self, params = None):
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
        response, _options = Api.send_request("POST", "/file_actions/move/{path}".format(path=params['path']), params, self.options)
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
    def begin_upload(self, params = None):
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
        response, _options = Api.send_request("POST", "/file_actions/begin_upload/{path}".format(path=params['path']), params, self.options)
        return response.data


# Copy file/folder
#
# Parameters:
#   destination (required) - string - Copy destination path.
#   structure - boolean - Copy structure only?
def copy(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "destination" in params and not isinstance(params["destination"], str):
        raise InvalidParameterError("Bad parameter: destination must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "destination" not in params:
        raise MissingParameterError("Parameter missing: destination")
    response, options = Api.send_request("POST", "/file_actions/copy/{path}".format(path=params['path']), params, options)
    return FileAction(response.data, options)

# Move file/folder
#
# Parameters:
#   destination (required) - string - Move destination path.
def move(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "destination" in params and not isinstance(params["destination"], str):
        raise InvalidParameterError("Bad parameter: destination must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "destination" not in params:
        raise MissingParameterError("Parameter missing: destination")
    response, options = Api.send_request("POST", "/file_actions/move/{path}".format(path=params['path']), params, options)
    return FileAction(response.data, options)

# Begin file upload
#
# Parameters:
#   mkdir_parents - boolean - Create parent directories if they do not exist?
#   part - int64 - Part if uploading a part.
#   parts - int64 - How many parts to fetch?
#   ref - string -
#   restart - int64 - File byte offset to restart from.
#   with_rename - boolean - Allow file rename instead of overwrite?
def begin_upload(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
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
    return [ FileUploadPart(entity_data, options) for entity_data in response.data ]

def new(*args, **kwargs):
    return FileAction(*args, **kwargs)
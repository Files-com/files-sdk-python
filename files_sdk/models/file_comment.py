import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FileComment:
    default_attributes = {
        'id': None,     # int64 - File Comment ID
        'body': None,     # string - Comment body.
        'reactions': None,     # FileCommentReaction - Reactions to this comment.
        'path': None,     # string - File path.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FileComment.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FileComment.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   body (required) - string - Comment body.
    def update(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "body" not in params:
            raise MissingParameterError("Parameter missing: body")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "body" in params and not isinstance(params["body"], str):
            raise InvalidParameterError("Bad parameter: body must be an str")
        response, _options = Api.send_request("PATCH", "/file_comments/{id}".format(id=params['id']), params, self.options)
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
        response, _options = Api.send_request("DELETE", "/file_comments/{id}".format(id=params['id']), params, self.options)
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
#   path (required) - string - Path to operate on.
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
    return ListObj(FileComment,"GET", "/file_comments/files/{path}".format(path=params['path']), params, options)

# Parameters:
#   body (required) - string - Comment body.
#   path (required) - string - File path.
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "body" in params and not isinstance(params["body"], str):
        raise InvalidParameterError("Bad parameter: body must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "body" not in params:
        raise MissingParameterError("Parameter missing: body")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    response, options = Api.send_request("POST", "/file_comments", params, options)
    return FileComment(response.data, options)

# Parameters:
#   body (required) - string - Comment body.
def update(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "body" in params and not isinstance(params["body"], str):
        raise InvalidParameterError("Bad parameter: body must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "body" not in params:
        raise MissingParameterError("Parameter missing: body")
    response, options = Api.send_request("PATCH", "/file_comments/{id}".format(id=params['id']), params, options)
    return FileComment(response.data, options)

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
    response, _options = Api.send_request("DELETE", "/file_comments/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = None, options = None):
    delete(id, params, options)

def new(*args, **kwargs):
    return FileComment(*args, **kwargs)
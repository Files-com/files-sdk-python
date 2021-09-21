import builtins
import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FileCommentReaction:
    default_attributes = {
        'id': None,     # int64 - Reaction ID
        'emoji': None,     # string - Emoji used in the reaction.
        'user_id': None,     # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        'file_comment_id': None,     # int64 - ID of file comment to attach reaction to.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FileCommentReaction.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FileCommentReaction.default_attributes if getattr(self, k, None) is not None}

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
        response, _options = Api.send_request("DELETE", "/file_comment_reactions/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The FileCommentReaction object doesn't support updates.")
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   file_comment_id (required) - int64 - ID of file comment to attach reaction to.
#   emoji (required) - string - Emoji to react with.
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "file_comment_id" in params and not isinstance(params["file_comment_id"], int):
        raise InvalidParameterError("Bad parameter: file_comment_id must be an int")
    if "emoji" in params and not isinstance(params["emoji"], str):
        raise InvalidParameterError("Bad parameter: emoji must be an str")
    if "file_comment_id" not in params:
        raise MissingParameterError("Parameter missing: file_comment_id")
    if "emoji" not in params:
        raise MissingParameterError("Parameter missing: emoji")
    response, options = Api.send_request("POST", "/file_comment_reactions", params, options)
    return FileCommentReaction(response.data, options)

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
    response, _options = Api.send_request("DELETE", "/file_comment_reactions/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = None, options = None):
    delete(id, params, options)

def new(*args, **kwargs):
    return FileCommentReaction(*args, **kwargs)
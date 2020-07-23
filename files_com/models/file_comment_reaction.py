import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class FileCommentReaction:
    default_attributes = {
        'id': None,     # int64 - Reaction ID
        'emoji': None,     # string - Emoji used in the reaction.
        'user_id': None,     # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        'file_comment_id': None,     # int64 - ID of file comment to attach reaction to.
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in FileCommentReaction.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in FileCommentReaction.default_attributes}

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
        return Api.send_request("DELETE", "/file_comment_reactions/{id}".format(id=params['id']), params, self.options)

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The FileCommentReaction object doesn't support updates.")
        else:
            new_obj = FileCommentReaction.do_create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

    # Parameters:
    #   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    #   file_comment_id (required) - int64 - ID of file comment to attach reaction to.
    #   emoji (required) - string - Emoji to react with.
    @staticmethod
    def do_create(params = {}, options = {}):
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
    
    @staticmethod
    def do_delete(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")

        response, _options = Api.send_request("DELETE", "/file_comment_reactions/{id}".format(id=params['id']), params, options)
        return response.data

    @staticmethod
    def do_destroy(id, params = {}):
        FileCommentReaction.do_delete(id, params)
    
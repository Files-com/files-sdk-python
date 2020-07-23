import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class MessageCommentReaction:
    default_attributes = {
        'id': None,     # int64 - Reaction ID
        'emoji': None,     # string - Emoji used in the reaction.
        'user_id': None,     # int64 - User ID.  Provide a value of `0` to operate the current session's user.
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in MessageCommentReaction.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in MessageCommentReaction.default_attributes}

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
        return Api.send_request("DELETE", "/message_comment_reactions/{id}".format(id=params['id']), params, self.options)

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The MessageCommentReaction object doesn't support updates.")
        else:
            new_obj = MessageCommentReaction.do_create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

    # Parameters:
    #   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    #   page - int64 - Current page number.
    #   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
    #   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
    #   message_comment_id (required) - int64 - Message comment to return reactions for.
    @staticmethod
    def do_list(params = {}, options = {}):
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        if "page" in params and not isinstance(params["page"], int):
            raise InvalidParameterError("Bad parameter: page must be an int")
        if "per_page" in params and not isinstance(params["per_page"], int):
            raise InvalidParameterError("Bad parameter: per_page must be an int")
        if "action" in params and not isinstance(params["action"], str):
            raise InvalidParameterError("Bad parameter: action must be an str")
        if "message_comment_id" in params and not isinstance(params["message_comment_id"], int):
            raise InvalidParameterError("Bad parameter: message_comment_id must be an int")
        if "message_comment_id" not in params:
            raise MissingParameterError("Parameter missing: message_comment_id")

        response, options = Api.send_request("GET", "/message_comment_reactions", params, options)
        return [ MessageCommentReaction(entity_data, options) for entity_data in response.data ]

    @staticmethod
    def do_all(params = {}):
        MessageCommentReaction.do_list(params)
    
    # Parameters:
    #   id (required) - int64 - Message Comment Reaction ID.
    @staticmethod
    def do_find(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")

        response, options = Api.send_request("GET", "/message_comment_reactions/{id}".format(id=params['id']), params, options)
        return MessageCommentReaction(response.data, options)

    @staticmethod
    def do_get(id, params = {}):
        MessageCommentReaction.do_find(id, params)
    
    # Parameters:
    #   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    #   emoji (required) - string - Emoji to react with.
    @staticmethod
    def do_create(params = {}, options = {}):
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        if "emoji" in params and not isinstance(params["emoji"], str):
            raise InvalidParameterError("Bad parameter: emoji must be an str")
        if "emoji" not in params:
            raise MissingParameterError("Parameter missing: emoji")

        response, options = Api.send_request("POST", "/message_comment_reactions", params, options)
        return MessageCommentReaction(response.data, options)
    
    @staticmethod
    def do_delete(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")

        response, _options = Api.send_request("DELETE", "/message_comment_reactions/{id}".format(id=params['id']), params, options)
        return response.data

    @staticmethod
    def do_destroy(id, params = {}):
        MessageCommentReaction.do_delete(id, params)
    
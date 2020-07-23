import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class GroupUser:
    default_attributes = {
        'group_name': None,     # string - Group name
        'group_id': None,     # int64 - Group ID
        'user_id': None,     # int64 - User ID
        'admin': None,     # boolean - Is this user an administrator of this group?
        'usernames': None,     # array - A list of usernames for users in this group
        'id': None,     # int64 - Group User ID.
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in GroupUser.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in GroupUser.default_attributes}

    # Parameters:
    #   group_id (required) - int64 - Group ID to add user to.
    #   user_id (required) - int64 - User ID to add to group.
    #   admin - boolean - Is the user a group administrator?
    def update(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and not isinstance(params["group_id"], int):
            raise InvalidParameterError("Bad parameter: group_id must be an int")
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        return Api.send_request("PATCH", "/group_users/{id}".format(id=params['id']), params, self.options)

    # Parameters:
    #   group_id (required) - int64 - Group ID from which to remove user.
    #   user_id (required) - int64 - User ID to remove from group.
    def delete(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and not isinstance(params["group_id"], int):
            raise InvalidParameterError("Bad parameter: group_id must be an int")
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        return Api.send_request("DELETE", "/group_users/{id}".format(id=params['id']), params, self.options)

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        self.update(self.get_attributes())

    # Parameters:
    #   user_id - int64 - User ID.  If provided, will return group_users of this user.
    #   page - int64 - Current page number.
    #   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
    #   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
    #   group_id - int64 - Group ID.  If provided, will return group_users of this group.
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
        if "group_id" in params and not isinstance(params["group_id"], int):
            raise InvalidParameterError("Bad parameter: group_id must be an int")

        response, options = Api.send_request("GET", "/group_users", params, options)
        return [ GroupUser(entity_data, options) for entity_data in response.data ]

    @staticmethod
    def do_all(params = {}):
        GroupUser.do_list(params)
    
    # Parameters:
    #   group_id (required) - int64 - Group ID to add user to.
    #   user_id (required) - int64 - User ID to add to group.
    #   admin - boolean - Is the user a group administrator?
    @staticmethod
    def do_update(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and not isinstance(params["group_id"], int):
            raise InvalidParameterError("Bad parameter: group_id must be an int")
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")

        response, options = Api.send_request("PATCH", "/group_users/{id}".format(id=params['id']), params, options)
        return GroupUser(response.data, options)
    
    # Parameters:
    #   group_id (required) - int64 - Group ID from which to remove user.
    #   user_id (required) - int64 - User ID to remove from group.
    @staticmethod
    def do_delete(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "group_id" in params and not isinstance(params["group_id"], int):
            raise InvalidParameterError("Bad parameter: group_id must be an int")
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "group_id" not in params:
            raise MissingParameterError("Parameter missing: group_id")
        if "user_id" not in params:
            raise MissingParameterError("Parameter missing: user_id")

        response, _options = Api.send_request("DELETE", "/group_users/{id}".format(id=params['id']), params, options)
        return response.data

    @staticmethod
    def do_destroy(id, params = {}):
        GroupUser.do_delete(id, params)
    
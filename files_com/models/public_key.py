import datetime
from files_com.api import Api
from files_com.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class PublicKey:
    default_attributes = {
        'id': None,     # int64 - Public key ID
        'title': None,     # string - Public key title
        'created_at': None,     # date-time - Public key created at date/time
        'fingerprint': None,     # string - Public key fingerprint
        'user_id': None,     # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        'public_key': None,     # string - Actual contents of SSH key.
    }

    def __init__(self, attributes, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in PublicKey.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in PublicKey.default_attributes}

    # Parameters:
    #   title (required) - string - Internal reference for key.
    def update(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "title" not in params:
            raise MissingParameterError("Parameter missing: title")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        return Api.send_request("PATCH", "/public_keys/{id}".format(id=params['id']), params, self.options)

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
        return Api.send_request("DELETE", "/public_keys/{id}".format(id=params['id']), params, self.options)

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = PublicKey.do_create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

    # Parameters:
    #   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    #   page - int64 - Current page number.
    #   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
    #   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
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

        response, options = Api.send_request("GET", "/public_keys", params, options)
        return [ PublicKey(entity_data, options) for entity_data in response.data ]

    @staticmethod
    def do_all(params = {}):
        PublicKey.do_list(params)
    
    # Parameters:
    #   id (required) - int64 - Public Key ID.
    @staticmethod
    def do_find(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")

        response, options = Api.send_request("GET", "/public_keys/{id}".format(id=params['id']), params, options)
        return PublicKey(response.data, options)

    @staticmethod
    def do_get(id, params = {}):
        PublicKey.do_find(id, params)
    
    # Parameters:
    #   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    #   title (required) - string - Internal reference for key.
    #   public_key (required) - string - Actual contents of SSH key.
    @staticmethod
    def do_create(params = {}, options = {}):
        if "user_id" in params and not isinstance(params["user_id"], int):
            raise InvalidParameterError("Bad parameter: user_id must be an int")
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        if "public_key" in params and not isinstance(params["public_key"], str):
            raise InvalidParameterError("Bad parameter: public_key must be an str")
        if "title" not in params:
            raise MissingParameterError("Parameter missing: title")
        if "public_key" not in params:
            raise MissingParameterError("Parameter missing: public_key")

        response, options = Api.send_request("POST", "/public_keys", params, options)
        return PublicKey(response.data, options)
    
    # Parameters:
    #   title (required) - string - Internal reference for key.
    @staticmethod
    def do_update(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "title" in params and not isinstance(params["title"], str):
            raise InvalidParameterError("Bad parameter: title must be an str")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "title" not in params:
            raise MissingParameterError("Parameter missing: title")

        response, options = Api.send_request("PATCH", "/public_keys/{id}".format(id=params['id']), params, options)
        return PublicKey(response.data, options)
    
    @staticmethod
    def do_delete(id, params = {}, options = {}):
        if not isinstance(params, dict):
            params = {}
        params["id"] = id
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")

        response, _options = Api.send_request("DELETE", "/public_keys/{id}".format(id=params['id']), params, options)
        return response.data

    @staticmethod
    def do_destroy(id, params = {}):
        PublicKey.do_delete(id, params)
    
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class As2Key:
    default_attributes = {
        'id': None,     # int64 - AS2 Key ID
        'as2_partnership_name': None,     # string - AS2 Partnership Name
        'created_at': None,     # date-time - AS2 Key created at date/time
        'fingerprint': None,     # string - Public key fingerprint
        'user_id': None,     # int64 - User ID.  Provide a value of `0` to operate the current session's user.
        'public_key': None,     # string - Actual contents of Public key.
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in As2Key.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in As2Key.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   as2_partnership_name (required) - string - AS2 Partnership Name
    def update(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "as2_partnership_name" not in params:
            raise MissingParameterError("Parameter missing: as2_partnership_name")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "as2_partnership_name" in params and not isinstance(params["as2_partnership_name"], str):
            raise InvalidParameterError("Bad parameter: as2_partnership_name must be an str")
        response, _options = Api.send_request("PATCH", "/as2_keys/{id}".format(id=params['id']), params, self.options)
        return response.data

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
        response, _options = Api.send_request("DELETE", "/as2_keys/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = {}):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   page - int64 - Current page number.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action - string - Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
#   cursor - string - Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
def list(params = {}, options = {}):
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "page" in params and not isinstance(params["page"], int):
        raise InvalidParameterError("Bad parameter: page must be an int")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    return ListObj(As2Key,"GET", "/as2_keys", params, options)

def all(params = {}, options = {}):
    list(params, options)

# Parameters:
#   id (required) - int64 - As2 Key ID.
def find(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("GET", "/as2_keys/{id}".format(id=params['id']), params, options)
    return As2Key(response.data, options)

def get(id, params = {}, options = {}):
    find(id, params, options)

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   as2_partnership_name (required) - string - AS2 Partnership Name
#   public_key (required) - string - Actual contents of Public key.
def create(params = {}, options = {}):
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "as2_partnership_name" in params and not isinstance(params["as2_partnership_name"], str):
        raise InvalidParameterError("Bad parameter: as2_partnership_name must be an str")
    if "public_key" in params and not isinstance(params["public_key"], str):
        raise InvalidParameterError("Bad parameter: public_key must be an str")
    if "as2_partnership_name" not in params:
        raise MissingParameterError("Parameter missing: as2_partnership_name")
    if "public_key" not in params:
        raise MissingParameterError("Parameter missing: public_key")
    response, options = Api.send_request("POST", "/as2_keys", params, options)
    return As2Key(response.data, options)

# Parameters:
#   as2_partnership_name (required) - string - AS2 Partnership Name
def update(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "as2_partnership_name" in params and not isinstance(params["as2_partnership_name"], str):
        raise InvalidParameterError("Bad parameter: as2_partnership_name must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "as2_partnership_name" not in params:
        raise MissingParameterError("Parameter missing: as2_partnership_name")
    response, options = Api.send_request("PATCH", "/as2_keys/{id}".format(id=params['id']), params, options)
    return As2Key(response.data, options)

def delete(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/as2_keys/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = {}, options = {}):
    delete(id, params, options)

def new(*args, **kwargs):
    return As2Key(*args, **kwargs)
import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class GpgKey:
    default_attributes = {
        'id': None,     # int64 - Your GPG key ID.
        'expires_at': None,     # date-time - Your GPG key expiration date.
        'name': None,     # string - Your GPG key name.
        'user_id': None,     # int64 - GPG owner's user id
        'public_key': None,     # string - Your GPG public key
        'private_key': None,     # string - Your GPG private key.
        'private_key_password': None,     # string - Your GPG private key password. Only required for password protected keys.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in GpgKey.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in GpgKey.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   name (required) - string - Your GPG key name.
    #   public_key - string - Your GPG public key
    #   private_key - string - Your GPG private key.
    #   private_key_password - string - Your GPG private key password. Only required for password protected keys.
    def update(self, params = None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "name" not in params:
            raise MissingParameterError("Parameter missing: name")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "public_key" in params and not isinstance(params["public_key"], str):
            raise InvalidParameterError("Bad parameter: public_key must be an str")
        if "private_key" in params and not isinstance(params["private_key"], str):
            raise InvalidParameterError("Bad parameter: private_key must be an str")
        if "private_key_password" in params and not isinstance(params["private_key_password"], str):
            raise InvalidParameterError("Bad parameter: private_key_password must be an str")
        response, _options = Api.send_request("PATCH", "/gpg_keys/{id}".format(id=params['id']), params, self.options)
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
        response, _options = Api.send_request("DELETE", "/gpg_keys/{id}".format(id=params['id']), params, self.options)
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
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(GpgKey,"GET", "/gpg_keys", params, options)

def all(params = None, options = None):
    list(params, options)

# Parameters:
#   id (required) - int64 - Gpg Key ID.
def find(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("GET", "/gpg_keys/{id}".format(id=params['id']), params, options)
    return GpgKey(response.data, options)

def get(id, params = None, options = None):
    find(id, params, options)

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   name (required) - string - Your GPG key name.
#   public_key - string - Your GPG public key
#   private_key - string - Your GPG private key.
#   private_key_password - string - Your GPG private key password. Only required for password protected keys.
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "public_key" in params and not isinstance(params["public_key"], str):
        raise InvalidParameterError("Bad parameter: public_key must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError("Bad parameter: private_key must be an str")
    if "private_key_password" in params and not isinstance(params["private_key_password"], str):
        raise InvalidParameterError("Bad parameter: private_key_password must be an str")
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    response, options = Api.send_request("POST", "/gpg_keys", params, options)
    return GpgKey(response.data, options)

# Parameters:
#   name (required) - string - Your GPG key name.
#   public_key - string - Your GPG public key
#   private_key - string - Your GPG private key.
#   private_key_password - string - Your GPG private key password. Only required for password protected keys.
def update(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "public_key" in params and not isinstance(params["public_key"], str):
        raise InvalidParameterError("Bad parameter: public_key must be an str")
    if "private_key" in params and not isinstance(params["private_key"], str):
        raise InvalidParameterError("Bad parameter: private_key must be an str")
    if "private_key_password" in params and not isinstance(params["private_key_password"], str):
        raise InvalidParameterError("Bad parameter: private_key_password must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "name" not in params:
        raise MissingParameterError("Parameter missing: name")
    response, options = Api.send_request("PATCH", "/gpg_keys/{id}".format(id=params['id']), params, options)
    return GpgKey(response.data, options)

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
    response, _options = Api.send_request("DELETE", "/gpg_keys/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = None, options = None):
    delete(id, params, options)

def new(*args, **kwargs):
    return GpgKey(*args, **kwargs)
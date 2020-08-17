import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class UserCipherUse:
    default_attributes = {
        'id': None,     # int64 - UserCipherUse ID
        'protocol_cipher': None,     # string - The protocol and cipher employed
        'created_at': None,     # date-time - The earliest recorded use of this combination of interface and protocol and cipher (for this user)
        'interface': None,     # string - The interface accessed
        'updated_at': None,     # date-time - The most recent use of this combination of interface and protocol and cipher (for this user)
        'user_id': None,     # int64 - ID of the user who performed this access
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in UserCipherUse.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in UserCipherUse.default_attributes if getattr(self, k, None) is not None}


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
    return ListObj(UserCipherUse,"GET", "/user_cipher_uses", params, options)

def all(params = {}, options = {}):
    list(params, options)

def new(*args, **kwargs):
    return UserCipherUse(*args, **kwargs)
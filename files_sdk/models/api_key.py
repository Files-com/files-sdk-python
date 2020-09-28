import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class ApiKey:
    default_attributes = {
        'id': None,     # int64 - API Key ID
        'descriptive_label': None,     # string - Unique label that describes this API key.  Useful for external systems where you may have API keys from multiple accounts and want a human-readable label for each key.
        'created_at': None,     # date-time - Time which API Key was created
        'expires_at': None,     # date-time - API Key expiration date
        'key': None,     # string - API Key actual key string
        'last_use_at': None,     # date-time - API Key last used - note this value is only updated once per 3 hour period, so the 'actual' time of last use may be up to 3 hours later than this timestamp.
        'name': None,     # string - Internal name for the API Key.  For your use.
        'path': None,     # string - Folder path restriction for this api key. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'permission_set': None,     # string - Permissions for this API Key.  Keys with the `desktop_app` permission set only have the ability to do the functions provided in our Desktop App (File and Share Link operations).  Additional permission sets may become available in the future, such as for a Site Admin to give a key with no administrator privileges.  If you have ideas for permission sets, please let us know.
        'platform': None,     # string - If this API key represents a Desktop app, what platform was it created on?
        'user_id': None,     # int64 - User ID for the owner of this API Key.  May be blank for Site-wide API Keys.
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in ApiKey.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in ApiKey.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   name - string - Internal name for the API Key.  For your use.
    #   expires_at - string - API Key expiration date
    #   permission_set - string - Permissions for this API Key.  Keys with the `desktop_app` permission set only have the ability to do the functions provided in our Desktop App (File and Share Link operations).  Additional permission sets may become available in the future, such as for a Site Admin to give a key with no administrator privileges.  If you have ideas for permission sets, please let us know.
    def update(self, params = {}):
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
        if "name" in params and not isinstance(params["name"], str):
            raise InvalidParameterError("Bad parameter: name must be an str")
        if "expires_at" in params and not isinstance(params["expires_at"], str):
            raise InvalidParameterError("Bad parameter: expires_at must be an str")
        if "permission_set" in params and not isinstance(params["permission_set"], str):
            raise InvalidParameterError("Bad parameter: permission_set must be an str")
        response, _options = Api.send_request("PATCH", "/api_keys/{id}".format(id=params['id']), params, self.options)
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
        response, _options = Api.send_request("DELETE", "/api_keys/{id}".format(id=params['id']), params, self.options)
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
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `deleted_at` and `expires_at`.
#   filter - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `expires_at`.
#   filter_gt - object - If set, return records where the specifiied field is greater than the supplied value. Valid fields are `expires_at`.
#   filter_gteq - object - If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `expires_at`.
#   filter_like - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `expires_at`.
#   filter_lt - object - If set, return records where the specifiied field is less than the supplied value. Valid fields are `expires_at`.
#   filter_lteq - object - If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `expires_at`.
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
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_gt" in params and not isinstance(params["filter_gt"], dict):
        raise InvalidParameterError("Bad parameter: filter_gt must be an dict")
    if "filter_gteq" in params and not isinstance(params["filter_gteq"], dict):
        raise InvalidParameterError("Bad parameter: filter_gteq must be an dict")
    if "filter_like" in params and not isinstance(params["filter_like"], dict):
        raise InvalidParameterError("Bad parameter: filter_like must be an dict")
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError("Bad parameter: filter_lteq must be an dict")
    return ListObj(ApiKey,"GET", "/api_keys", params, options)

def all(params = {}, options = {}):
    list(params, options)

# Parameters:
#   format - string
#   api_key - object
def find_current(params = {}, options = {}):
    if "format" in params and not isinstance(params["format"], str):
        raise InvalidParameterError("Bad parameter: format must be an str")
    if "api_key" in params and not isinstance(params["api_key"], dict):
        raise InvalidParameterError("Bad parameter: api_key must be an dict")
    response, options = Api.send_request("GET", "/api_key", params, options)
    return ApiKey(response.data, options)

# Parameters:
#   id (required) - int64 - Api Key ID.
def find(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("GET", "/api_keys/{id}".format(id=params['id']), params, options)
    return ApiKey(response.data, options)

def get(id, params = {}, options = {}):
    find(id, params, options)

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   name - string - Internal name for the API Key.  For your use.
#   expires_at - string - API Key expiration date
#   permission_set - string - Permissions for this API Key.  Keys with the `desktop_app` permission set only have the ability to do the functions provided in our Desktop App (File and Share Link operations).  Additional permission sets may become available in the future, such as for a Site Admin to give a key with no administrator privileges.  If you have ideas for permission sets, please let us know.
#   path - string - Folder path restriction for this api key.
def create(params = {}, options = {}):
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "permission_set" in params and not isinstance(params["permission_set"], str):
        raise InvalidParameterError("Bad parameter: permission_set must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    response, options = Api.send_request("POST", "/api_keys", params, options)
    return ApiKey(response.data, options)

# Parameters:
#   expires_at - string - API Key expiration date
#   name - string - Internal name for the API Key.  For your use.
#   permission_set - string - Permissions for this API Key.  Keys with the `desktop_app` permission set only have the ability to do the functions provided in our Desktop App (File and Share Link operations).  Additional permission sets may become available in the future, such as for a Site Admin to give a key with no administrator privileges.  If you have ideas for permission sets, please let us know.
def update_current(params = {}, options = {}):
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "permission_set" in params and not isinstance(params["permission_set"], str):
        raise InvalidParameterError("Bad parameter: permission_set must be an str")
    response, options = Api.send_request("PATCH", "/api_key", params, options)
    return ApiKey(response.data, options)

# Parameters:
#   name - string - Internal name for the API Key.  For your use.
#   expires_at - string - API Key expiration date
#   permission_set - string - Permissions for this API Key.  Keys with the `desktop_app` permission set only have the ability to do the functions provided in our Desktop App (File and Share Link operations).  Additional permission sets may become available in the future, such as for a Site Admin to give a key with no administrator privileges.  If you have ideas for permission sets, please let us know.
def update(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "name" in params and not isinstance(params["name"], str):
        raise InvalidParameterError("Bad parameter: name must be an str")
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "permission_set" in params and not isinstance(params["permission_set"], str):
        raise InvalidParameterError("Bad parameter: permission_set must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("PATCH", "/api_keys/{id}".format(id=params['id']), params, options)
    return ApiKey(response.data, options)

# Parameters:
#   format - string
#   api_key - object
def delete_current(params = {}, options = {}):
    if "format" in params and not isinstance(params["format"], str):
        raise InvalidParameterError("Bad parameter: format must be an str")
    if "api_key" in params and not isinstance(params["api_key"], dict):
        raise InvalidParameterError("Bad parameter: api_key must be an dict")
    response, _options = Api.send_request("DELETE", "/api_key", params, options)
    return response.data

def delete(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/api_keys/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = {}, options = {}):
    delete(id, params, options)

def new(*args, **kwargs):
    return ApiKey(*args, **kwargs)
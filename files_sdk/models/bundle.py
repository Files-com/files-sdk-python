import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Bundle:
    default_attributes = {
        'code': None,     # string - Bundle code.  This code forms the end part of the Public URL.
        'url': None,     # string - Public URL of Share Link
        'description': None,     # string - Public description
        'password_protected': None,     # boolean - Is this bundle password protected?
        'require_registration': None,     # boolean - Show a registration page that captures the downloader's name and email address?
        'require_share_recipient': None,     # boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
        'clickwrap_body': None,     # string - Legal text that must be agreed to prior to accessing Bundle.
        'id': None,     # int64 - Bundle ID
        'created_at': None,     # date-time - Bundle created at date/time
        'expires_at': None,     # date-time - Bundle expiration date/time
        'max_uses': None,     # int64 - Maximum number of times bundle can be accessed
        'note': None,     # string - Bundle internal note
        'user_id': None,     # int64 - Bundle creator user ID
        'username': None,     # string - Bundle creator username
        'clickwrap_id': None,     # int64 - ID of the clickwrap to use with this bundle.
        'inbox_id': None,     # int64 - ID of the associated inbox, if available.
        'paths': None,     # array - A list of paths in this bundle
        'password': None,     # string - Password for this bundle.
    }

    def __init__(self, attributes={}, options={}):
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Bundle.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Bundle.default_attributes if getattr(self, k, None) is not None}

    # Send email(s) with a link to bundle
    #
    # Parameters:
    #   to (required) - array(string) - A list of email addresses to share this bundle with.
    #   note - string - Note to include in email.
    def share(self, params = {}):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params['id'] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "to" not in params:
            raise MissingParameterError("Parameter missing: to")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "to" in params and not isinstance(params["to"], list):
            raise InvalidParameterError("Bad parameter: to must be an list")
        if "note" in params and not isinstance(params["note"], str):
            raise InvalidParameterError("Bad parameter: note must be an str")
        response, _options = Api.send_request("POST", "/bundles/{id}/share".format(id=params['id']), params, self.options)
        return response.data

    # Parameters:
    #   password - string - Password for this bundle.
    #   clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
    #   code - string - Bundle code.  This code forms the end part of the Public URL.
    #   description - string - Public description
    #   expires_at - string - Bundle expiration date/time
    #   inbox_id - int64 - ID of the associated inbox, if available.
    #   max_uses - int64 - Maximum number of times bundle can be accessed
    #   note - string - Bundle internal note
    #   require_registration - boolean - Show a registration page that captures the downloader's name and email address?
    #   require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
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
        if "password" in params and not isinstance(params["password"], str):
            raise InvalidParameterError("Bad parameter: password must be an str")
        if "clickwrap_id" in params and not isinstance(params["clickwrap_id"], int):
            raise InvalidParameterError("Bad parameter: clickwrap_id must be an int")
        if "code" in params and not isinstance(params["code"], str):
            raise InvalidParameterError("Bad parameter: code must be an str")
        if "description" in params and not isinstance(params["description"], str):
            raise InvalidParameterError("Bad parameter: description must be an str")
        if "expires_at" in params and not isinstance(params["expires_at"], str):
            raise InvalidParameterError("Bad parameter: expires_at must be an str")
        if "inbox_id" in params and not isinstance(params["inbox_id"], int):
            raise InvalidParameterError("Bad parameter: inbox_id must be an int")
        if "max_uses" in params and not isinstance(params["max_uses"], int):
            raise InvalidParameterError("Bad parameter: max_uses must be an int")
        if "note" in params and not isinstance(params["note"], str):
            raise InvalidParameterError("Bad parameter: note must be an str")
        response, _options = Api.send_request("PATCH", "/bundles/{id}".format(id=params['id']), params, self.options)
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
        response, _options = Api.send_request("DELETE", "/bundles/{id}".format(id=params['id']), params, self.options)
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
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `site_id`, `created_at` or `code`.
#   filter - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `created_at`.
#   filter_gt - object - If set, return records where the specifiied field is greater than the supplied value. Valid fields are `created_at`.
#   filter_gteq - object - If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `created_at`.
#   filter_like - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `created_at`.
#   filter_lt - object - If set, return records where the specifiied field is less than the supplied value. Valid fields are `created_at`.
#   filter_lteq - object - If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `created_at`.
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
    return ListObj(Bundle,"GET", "/bundles", params, options)

def all(params = {}, options = {}):
    list(params, options)

# Parameters:
#   id (required) - int64 - Bundle ID.
def find(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("GET", "/bundles/{id}".format(id=params['id']), params, options)
    return Bundle(response.data, options)

def get(id, params = {}, options = {}):
    find(id, params, options)

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   paths (required) - array(string) - A list of paths to include in this bundle.
#   password - string - Password for this bundle.
#   expires_at - string - Bundle expiration date/time
#   max_uses - int64 - Maximum number of times bundle can be accessed
#   description - string - Public description
#   note - string - Bundle internal note
#   code - string - Bundle code.  This code forms the end part of the Public URL.
#   require_registration - boolean - Show a registration page that captures the downloader's name and email address?
#   clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
#   inbox_id - int64 - ID of the associated inbox, if available.
#   require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
def create(params = {}, options = {}):
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "paths" in params and not isinstance(params["paths"], list):
        raise InvalidParameterError("Bad parameter: paths must be an list")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "max_uses" in params and not isinstance(params["max_uses"], int):
        raise InvalidParameterError("Bad parameter: max_uses must be an int")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError("Bad parameter: description must be an str")
    if "note" in params and not isinstance(params["note"], str):
        raise InvalidParameterError("Bad parameter: note must be an str")
    if "code" in params and not isinstance(params["code"], str):
        raise InvalidParameterError("Bad parameter: code must be an str")
    if "clickwrap_id" in params and not isinstance(params["clickwrap_id"], int):
        raise InvalidParameterError("Bad parameter: clickwrap_id must be an int")
    if "inbox_id" in params and not isinstance(params["inbox_id"], int):
        raise InvalidParameterError("Bad parameter: inbox_id must be an int")
    if "paths" not in params:
        raise MissingParameterError("Parameter missing: paths")
    response, options = Api.send_request("POST", "/bundles", params, options)
    return Bundle(response.data, options)

# Send email(s) with a link to bundle
#
# Parameters:
#   to (required) - array(string) - A list of email addresses to share this bundle with.
#   note - string - Note to include in email.
def share(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "to" in params and not isinstance(params["to"], list):
        raise InvalidParameterError("Bad parameter: to must be an list")
    if "note" in params and not isinstance(params["note"], str):
        raise InvalidParameterError("Bad parameter: note must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    if "to" not in params:
        raise MissingParameterError("Parameter missing: to")
    response, _options = Api.send_request("POST", "/bundles/{id}/share".format(id=params['id']), params, options)
    return response.data

# Parameters:
#   password - string - Password for this bundle.
#   clickwrap_id - int64 - ID of the clickwrap to use with this bundle.
#   code - string - Bundle code.  This code forms the end part of the Public URL.
#   description - string - Public description
#   expires_at - string - Bundle expiration date/time
#   inbox_id - int64 - ID of the associated inbox, if available.
#   max_uses - int64 - Maximum number of times bundle can be accessed
#   note - string - Bundle internal note
#   require_registration - boolean - Show a registration page that captures the downloader's name and email address?
#   require_share_recipient - boolean - Only allow access to recipients who have explicitly received the share via an email sent through the Files.com UI?
def update(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "password" in params and not isinstance(params["password"], str):
        raise InvalidParameterError("Bad parameter: password must be an str")
    if "clickwrap_id" in params and not isinstance(params["clickwrap_id"], int):
        raise InvalidParameterError("Bad parameter: clickwrap_id must be an int")
    if "code" in params and not isinstance(params["code"], str):
        raise InvalidParameterError("Bad parameter: code must be an str")
    if "description" in params and not isinstance(params["description"], str):
        raise InvalidParameterError("Bad parameter: description must be an str")
    if "expires_at" in params and not isinstance(params["expires_at"], str):
        raise InvalidParameterError("Bad parameter: expires_at must be an str")
    if "inbox_id" in params and not isinstance(params["inbox_id"], int):
        raise InvalidParameterError("Bad parameter: inbox_id must be an int")
    if "max_uses" in params and not isinstance(params["max_uses"], int):
        raise InvalidParameterError("Bad parameter: max_uses must be an int")
    if "note" in params and not isinstance(params["note"], str):
        raise InvalidParameterError("Bad parameter: note must be an str")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("PATCH", "/bundles/{id}".format(id=params['id']), params, options)
    return Bundle(response.data, options)

def delete(id, params = {}, options = {}):
    if not isinstance(params, dict):
        params = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, _options = Api.send_request("DELETE", "/bundles/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = {}, options = {}):
    delete(id, params, options)

def new(*args, **kwargs):
    return Bundle(*args, **kwargs)
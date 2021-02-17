import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Behavior:
    default_attributes = {
        'id': None,     # int64 - Folder behavior ID
        'path': None,     # string - Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'attachment_url': None,     # string - URL for attached file
        'behavior': None,     # string - Behavior type.
        'value': None,     # object - Settings for this behavior.  See the section above for an example value to provide here.  Formatting is different for each Behavior type.  May be sent as nested JSON or a single JSON-encoded string.  If using XML encoding for the API call, this data must be sent as a JSON-encoded string.
        'attachment_file': None,     # file - Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Behavior.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Behavior.default_attributes if getattr(self, k, None) is not None}

    # Parameters:
    #   value - string - The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior.
    #   attachment_file - file - Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
    #   behavior - string - Behavior type.
    #   path - string - Folder behaviors path.
    def update(self, params = None):
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
        if "value" in params and not isinstance(params["value"], str):
            raise InvalidParameterError("Bad parameter: value must be an str")
        if "behavior" in params and not isinstance(params["behavior"], str):
            raise InvalidParameterError("Bad parameter: behavior must be an str")
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        response, _options = Api.send_request("PATCH", "/behaviors/{id}".format(id=params['id']), params, self.options)
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
        response, _options = Api.send_request("DELETE", "/behaviors/{id}".format(id=params['id']), params, self.options)
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
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `behavior`.
#   filter - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `behavior`.
#   filter_gt - object - If set, return records where the specifiied field is greater than the supplied value. Valid fields are `behavior`.
#   filter_gteq - object - If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `behavior`.
#   filter_like - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `behavior`.
#   filter_lt - object - If set, return records where the specifiied field is less than the supplied value. Valid fields are `behavior`.
#   filter_lteq - object - If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `behavior`.
#   behavior - string - If set, only shows folder behaviors matching this behavior type.
def list(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
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
    if "behavior" in params and not isinstance(params["behavior"], str):
        raise InvalidParameterError("Bad parameter: behavior must be an str")
    return ListObj(Behavior,"GET", "/behaviors", params, options)

def all(params = None, options = None):
    list(params, options)

# Parameters:
#   id (required) - int64 - Behavior ID.
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
    response, options = Api.send_request("GET", "/behaviors/{id}".format(id=params['id']), params, options)
    return Behavior(response.data, options)

def get(id, params = None, options = None):
    find(id, params, options)

# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `behavior`.
#   filter - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `behavior`.
#   filter_gt - object - If set, return records where the specifiied field is greater than the supplied value. Valid fields are `behavior`.
#   filter_gteq - object - If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `behavior`.
#   filter_like - object - If set, return records where the specifiied field is equal to the supplied value. Valid fields are `behavior`.
#   filter_lt - object - If set, return records where the specifiied field is less than the supplied value. Valid fields are `behavior`.
#   filter_lteq - object - If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `behavior`.
#   path (required) - string - Path to operate on.
#   recursive - string - Show behaviors above this path?
#   behavior - string - DEPRECATED: If set only shows folder behaviors matching this behavior type. Use `filter[behavior]` instead.
def list_for(path, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["path"] = path
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
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
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "recursive" in params and not isinstance(params["recursive"], str):
        raise InvalidParameterError("Bad parameter: recursive must be an str")
    if "behavior" in params and not isinstance(params["behavior"], str):
        raise InvalidParameterError("Bad parameter: behavior must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(Behavior,"GET", "/behaviors/folders/{path}".format(path=params['path']), params, options)

# Parameters:
#   value - string - The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior.
#   attachment_file - file - Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
#   path (required) - string - Folder behaviors path.
#   behavior (required) - string - Behavior type.
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "value" in params and not isinstance(params["value"], str):
        raise InvalidParameterError("Bad parameter: value must be an str")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "behavior" in params and not isinstance(params["behavior"], str):
        raise InvalidParameterError("Bad parameter: behavior must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "behavior" not in params:
        raise MissingParameterError("Parameter missing: behavior")
    response, options = Api.send_request("POST", "/behaviors", params, options)
    return Behavior(response.data, options)

# Parameters:
#   url (required) - string - URL for testing the webhook.
#   method - string - HTTP method(GET or POST).
#   encoding - string - HTTP encoding method.  Can be JSON, XML, or RAW (form data).
#   headers - object - Additional request headers.
#   body - object - Additional body parameters.
#   action - string - action for test body
def webhook_test(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "url" in params and not isinstance(params["url"], str):
        raise InvalidParameterError("Bad parameter: url must be an str")
    if "method" in params and not isinstance(params["method"], str):
        raise InvalidParameterError("Bad parameter: method must be an str")
    if "encoding" in params and not isinstance(params["encoding"], str):
        raise InvalidParameterError("Bad parameter: encoding must be an str")
    if "headers" in params and not isinstance(params["headers"], dict):
        raise InvalidParameterError("Bad parameter: headers must be an dict")
    if "body" in params and not isinstance(params["body"], dict):
        raise InvalidParameterError("Bad parameter: body must be an dict")
    if "action" in params and not isinstance(params["action"], str):
        raise InvalidParameterError("Bad parameter: action must be an str")
    if "url" not in params:
        raise MissingParameterError("Parameter missing: url")
    response, _options = Api.send_request("POST", "/behaviors/webhook/test", params, options)
    return response.data

# Parameters:
#   value - string - The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior.
#   attachment_file - file - Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
#   behavior - string - Behavior type.
#   path - string - Folder behaviors path.
def update(id, params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], (str, int, dict)): 
        raise InvalidParameterError("Bad parameter: id must be one of str, int, dict")
    if "value" in params and not isinstance(params["value"], str):
        raise InvalidParameterError("Bad parameter: value must be an str")
    if "behavior" in params and not isinstance(params["behavior"], str):
        raise InvalidParameterError("Bad parameter: behavior must be an str")
    if "path" in params and not isinstance(params["path"], (str, int, dict)): 
        raise InvalidParameterError("Bad parameter: path must be one of str, int, dict")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request("PATCH", "/behaviors/{id}".format(id=params['id']), params, options)
    return Behavior(response.data, options)

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
    response, _options = Api.send_request("DELETE", "/behaviors/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = None, options = None):
    delete(id, params, options)

def new(*args, **kwargs):
    return Behavior(*args, **kwargs)
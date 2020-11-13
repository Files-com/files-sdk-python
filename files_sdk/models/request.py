import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class Request:
    default_attributes = {
        'id': None,     # int64 - Request ID
        'path': None,     # string - Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'source': None,     # string - Source filename, if applicable
        'destination': None,     # string - Destination filename
        'automation_id': None,     # string - ID of automation that created request
        'user_display_name': None,     # string - User making the request (if applicable)
        'user_ids': None,     # string - A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
        'group_ids': None,     # string - A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in Request.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in Request.default_attributes if getattr(self, k, None) is not None}

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
        response, _options = Api.send_request("DELETE", "/requests/{id}".format(id=params['id']), params, self.options)
        return response.data

    def destroy(self, params = None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The Request object doesn't support updates.")
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `site_id`, `folder_id` or `destination`.
#   mine - boolean - Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
#   path - string - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.
def list(params = None, options = None):
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    return ListObj(Request,"GET", "/requests", params, options)

def all(params = None, options = None):
    list(params, options)

# Parameters:
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `site_id`, `folder_id` or `destination`.
#   mine - boolean - Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
#   path (required) - string - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.
def get_folder(path, params = None, options = None):
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
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    return ListObj(Request,"GET", "/requests/folders/{path}".format(path=params['path']), params, options)

# Parameters:
#   path (required) - string - Folder path on which to request the file.
#   destination (required) - string - Destination filename (without extension) to request.
#   user_ids - string - A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
#   group_ids - string - A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.
def create(params = None, options = None):
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "destination" in params and not isinstance(params["destination"], str):
        raise InvalidParameterError("Bad parameter: destination must be an str")
    if "user_ids" in params and not isinstance(params["user_ids"], str):
        raise InvalidParameterError("Bad parameter: user_ids must be an str")
    if "group_ids" in params and not isinstance(params["group_ids"], str):
        raise InvalidParameterError("Bad parameter: group_ids must be an str")
    if "path" not in params:
        raise MissingParameterError("Parameter missing: path")
    if "destination" not in params:
        raise MissingParameterError("Parameter missing: destination")
    response, options = Api.send_request("POST", "/requests", params, options)
    return Request(response.data, options)

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
    response, _options = Api.send_request("DELETE", "/requests/{id}".format(id=params['id']), params, options)
    return response.data

def destroy(id, params = None, options = None):
    delete(id, params, options)

def new(*args, **kwargs):
    return Request(*args, **kwargs)
import builtins
import datetime
from files_sdk.api import Api
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class ActionNotificationExport:
    default_attributes = {
        'id': None,     # int64 - History Export ID
        'export_version': None,     # string - Version of the underlying records for the export.
        'start_at': None,     # date-time - Start date/time of export range.
        'end_at': None,     # date-time - End date/time of export range.
        'status': None,     # string - Status of export.  Valid values: `building`, `ready`, or `failed`
        'query_path': None,     # string - Return notifications that were triggered by actions on this specific path.
        'query_folder': None,     # string - Return notifications that were triggered by actions in this folder.
        'query_message': None,     # string - Error message associated with the request, if any.
        'query_request_method': None,     # string - The HTTP request method used by the webhook.
        'query_request_url': None,     # string - The target webhook URL.
        'query_status': None,     # string - The HTTP status returned from the server in response to the webhook request.
        'query_success': None,     # boolean - true if the webhook request succeeded (i.e. returned a 200 or 204 response status). false otherwise.
        'results_url': None,     # string - If `status` is `ready`, this will be a URL where all the results can be downloaded at once as a CSV.
        'user_id': None,     # int64 - User ID.  Provide a value of `0` to operate the current session's user.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in ActionNotificationExport.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in ActionNotificationExport.default_attributes if getattr(self, k, None) is not None}

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError("The ActionNotificationExport object doesn't support updates.")
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())

# Parameters:
#   id (required) - int64 - Action Notification Export ID.
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
    response, options = Api.send_request("GET", "/action_notification_exports/{id}".format(id=params['id']), params, options)
    return ActionNotificationExport(response.data, options)

def get(id, params = None, options = None):
    find(id, params, options)

# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   start_at - string - Start date/time of export range.
#   end_at - string - End date/time of export range.
#   query_message - string - Error message associated with the request, if any.
#   query_request_method - string - The HTTP request method used by the webhook.
#   query_request_url - string - The target webhook URL.
#   query_status - string - The HTTP status returned from the server in response to the webhook request.
#   query_success - boolean - true if the webhook request succeeded (i.e. returned a 200 or 204 response status). false otherwise.
#   query_path - string - Return notifications that were triggered by actions on this specific path.
#   query_folder - string - Return notifications that were triggered by actions in this folder.
def create(params = None, options = None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "start_at" in params and not isinstance(params["start_at"], str):
        raise InvalidParameterError("Bad parameter: start_at must be an str")
    if "end_at" in params and not isinstance(params["end_at"], str):
        raise InvalidParameterError("Bad parameter: end_at must be an str")
    if "query_message" in params and not isinstance(params["query_message"], str):
        raise InvalidParameterError("Bad parameter: query_message must be an str")
    if "query_request_method" in params and not isinstance(params["query_request_method"], str):
        raise InvalidParameterError("Bad parameter: query_request_method must be an str")
    if "query_request_url" in params and not isinstance(params["query_request_url"], str):
        raise InvalidParameterError("Bad parameter: query_request_url must be an str")
    if "query_status" in params and not isinstance(params["query_status"], str):
        raise InvalidParameterError("Bad parameter: query_status must be an str")
    if "query_path" in params and not isinstance(params["query_path"], str):
        raise InvalidParameterError("Bad parameter: query_path must be an str")
    if "query_folder" in params and not isinstance(params["query_folder"], str):
        raise InvalidParameterError("Bad parameter: query_folder must be an str")
    response, options = Api.send_request("POST", "/action_notification_exports", params, options)
    return ActionNotificationExport(response.data, options)

def new(*args, **kwargs):
    return ActionNotificationExport(*args, **kwargs)
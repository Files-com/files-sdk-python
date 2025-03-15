import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ExternalEvent:
    default_attributes = {
        "id": None,  # int64 - Event ID
        "event_type": None,  # string - Type of event being recorded.
        "status": None,  # string - Status of event.
        "body": None,  # string - Event body
        "created_at": None,  # date-time - External event create date/time
        "body_url": None,  # string - Link to log file.
        "folder_behavior_id": None,  # int64 - Folder Behavior ID
        "siem_http_destination_id": None,  # int64 - SIEM HTTP Destination ID.
        "successful_files": None,  # int64 - For sync events, the number of files handled successfully.
        "errored_files": None,  # int64 - For sync events, the number of files that encountered errors.
        "bytes_synced": None,  # int64 - For sync events, the total number of bytes synced.
        "compared_files": None,  # int64 - For sync events, the number of files considered for the sync.
        "compared_folders": None,  # int64 - For sync events, the number of folders listed and considered for the sync.
        "remote_server_type": None,  # string - Associated Remote Server type, if any
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (
            attribute,
            default_value,
        ) in ExternalEvent.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in ExternalEvent.default_attributes
            if getattr(self, k, None) is not None
        }

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The ExternalEvent object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `siem_http_destination_id`, `created_at`, `event_type`, `status` or `folder_behavior_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status`, `folder_behavior_id` or `siem_http_destination_id`. Valid field combinations are `[ event_type, created_at ]`, `[ remote_server_type, created_at ]`, `[ status, created_at ]`, `[ folder_behavior_id, created_at ]`, `[ event_type, status ]`, `[ remote_server_type, status ]`, `[ folder_behavior_id, status ]`, `[ event_type, status, created_at ]`, `[ remote_server_type, status, created_at ]` or `[ folder_behavior_id, status, created_at ]`.
#   filter_gt - object - If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
#   filter_gteq - object - If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
#   filter_lt - object - If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
#   filter_lteq - object - If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
def list(params=None, options=None):
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
        raise InvalidParameterError(
            "Bad parameter: filter_gteq must be an dict"
        )
    if "filter_lt" in params and not isinstance(params["filter_lt"], dict):
        raise InvalidParameterError("Bad parameter: filter_lt must be an dict")
    if "filter_lteq" in params and not isinstance(params["filter_lteq"], dict):
        raise InvalidParameterError(
            "Bad parameter: filter_lteq must be an dict"
        )
    return ListObj(ExternalEvent, "GET", "/external_events", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - External Event ID.
def find(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "GET", "/external_events/{id}".format(id=params["id"]), params, options
    )
    return ExternalEvent(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   status (required) - string - Status of event.
#   body (required) - string - Event body
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "status" in params and not isinstance(params["status"], str):
        raise InvalidParameterError("Bad parameter: status must be an str")
    if "body" in params and not isinstance(params["body"], str):
        raise InvalidParameterError("Bad parameter: body must be an str")
    if "status" not in params:
        raise MissingParameterError("Parameter missing: status")
    if "body" not in params:
        raise MissingParameterError("Parameter missing: body")
    response, options = Api.send_request(
        "POST", "/external_events", params, options
    )
    return ExternalEvent(response.data, options)


def new(*args, **kwargs):
    return ExternalEvent(*args, **kwargs)

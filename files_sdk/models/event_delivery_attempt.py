import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class EventDeliveryAttempt:
    default_attributes = {
        "id": None,  # int64 - Event Delivery Attempt ID
        "event_record_id": None,  # int64 - Event Record ID
        "event_subscription_id": None,  # int64 - Event Subscription ID
        "event_target_id": None,  # int64 - Event Target ID
        "workspace_id": None,  # int64 - Workspace ID. 0 means the default workspace or site-wide.
        "status": None,  # string - Delivery status.
        "attempt_number": None,  # int64 - Number of delivery attempts made.
        "response_code": None,  # int64 - HTTP response code, if applicable.
        "error_message": None,  # string - Delivery error message, if applicable.
        "response_body": None,  # string - Delivery response body, if applicable.
        "latency_ms": None,  # int64 - Delivery latency in milliseconds.
        "delivered_at": None,  # date-time - Successful delivery date/time.
        "last_attempted_at": None,  # date-time - Most recent attempt date/time.
        "next_attempt_at": None,  # date-time - Next scheduled attempt date/time.
        "created_at": None,  # date-time - Delivery Attempt create date/time.
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
        ) in EventDeliveryAttempt.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in EventDeliveryAttempt.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `status`, `event_record_id`, `event_target_id` or `workspace_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `status`, `workspace_id`, `event_record_id` or `event_target_id`. Valid field combinations are `[ workspace_id, status ]`, `[ workspace_id, event_record_id ]` or `[ workspace_id, event_target_id ]`.
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
    return ListObj(
        EventDeliveryAttempt,
        "GET",
        "/event_delivery_attempts",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Event Delivery Attempt ID.
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
        "GET",
        "/event_delivery_attempts/{id}".format(id=params["id"]),
        params,
        options,
    )
    return EventDeliveryAttempt(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


def new(*args, **kwargs):
    return EventDeliveryAttempt(*args, **kwargs)

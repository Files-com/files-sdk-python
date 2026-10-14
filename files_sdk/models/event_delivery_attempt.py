import builtins  # noqa: F401
from typing import Any, Mapping  # noqa: F401
from files_sdk.api import (  # noqa: F401
    LEGACY,
    LegacyScope,
    Operation,
    copy_params,
    decode_record,
    path_value,
)
from files_sdk.api_client import unexpected_response_error  # noqa: F401
from files_sdk.context import RequestOptions  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class EventDeliveryAttempt:
    """A event delivery attempt record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Event Delivery Attempt ID
        event_record_id: int64 - Event Record ID
        event_subscription_id: int64 - Event Subscription ID
        event_target_id: int64 - Event Target ID
        activity_notification_batch_id: int64 - Shared summary ID when this event is delivered in a Slack or Teams subfolder summary. All events in a summary share its delivery outcome.
        workspace_id: int64 - Workspace ID. 0 means the default workspace or site-wide.
        status: string - Delivery status.
        attempt_number: int64 - Number of delivery attempts made.
        response_code: int64 - HTTP response code, if applicable.
        error_message: string - Delivery error message, if applicable.
        response_body: string - Delivery response body, if applicable.
        latency_ms: int64 - Delivery latency in milliseconds.
        delivered_at: date-time - Successful delivery date/time.
        last_attempted_at: date-time - Most recent attempt date/time.
        next_attempt_at: date-time - Next scheduled attempt date/time.
        created_at: date-time - Delivery Attempt create date/time.
    """

    default_attributes = {
        "id": None,  # int64 - Event Delivery Attempt ID
        "event_record_id": None,  # int64 - Event Record ID
        "event_subscription_id": None,  # int64 - Event Subscription ID
        "event_target_id": None,  # int64 - Event Target ID
        "activity_notification_batch_id": None,  # int64 - Shared summary ID when this event is delivered in a Slack or Teams subfolder summary. All events in a summary share its delivery outcome.
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

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    event_record_id: int | None
    event_subscription_id: int | None
    event_target_id: int | None
    activity_notification_batch_id: int | None
    workspace_id: int | None
    status: str | None
    attempt_number: int | None
    response_code: int | None
    error_message: str | None
    response_body: str | None
    latency_ms: int | None
    delivered_at: str | None
    last_attempted_at: str | None
    next_attempt_at: str | None
    created_at: str | None

    # The client and settings this object's operations use: those of the
    # operation or client that made it, or the module's when it starts an
    # operation if neither did.
    _context: Any = None

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = dict(options)

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

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class EventDeliveryAttemptResource:
    """EventDeliveryAttempt operations that use one client's configuration.

    Get one from a client, such as ``client.event_delivery_attempt``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[EventDeliveryAttempt]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `status`, `event_record_id`, `event_target_id` or `workspace_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `status`, `workspace_id`, `event_record_id` or `event_target_id`. Valid field combinations are `[ workspace_id, status ]`, `[ workspace_id, event_record_id ]` or `[ workspace_id, event_target_id ]`.
        """
        params = copy_params(params)
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "sort_by" in params and not isinstance(params["sort_by"], dict):
            raise InvalidParameterError(
                "Bad parameter: sort_by must be an dict"
            )
        if "filter" in params and not isinstance(params["filter"], dict):
            raise InvalidParameterError(
                "Bad parameter: filter must be an dict"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            EventDeliveryAttempt,
            "GET",
            "/event_delivery_attempts",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[EventDeliveryAttempt]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventDeliveryAttempt:
        """Parameters:
        id (required) - int64 - Event Delivery Attempt ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> EventDeliveryAttempt:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET",
            "/event_delivery_attempts/" + path_value(params["id"]),
            params,
        )
        return operation.decode_model(response, EventDeliveryAttempt)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventDeliveryAttempt:
        """The same as find()."""
        return self.find(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> EventDeliveryAttempt:
        """A new EventDeliveryAttempt with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = EventDeliveryAttempt(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = EventDeliveryAttemptResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[EventDeliveryAttempt]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `status`, `event_record_id`, `event_target_id` or `workspace_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `status`, `workspace_id`, `event_record_id` or `event_target_id`. Valid field combinations are `[ workspace_id, status ]`, `[ workspace_id, event_record_id ]` or `[ workspace_id, event_target_id ]`.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[EventDeliveryAttempt]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventDeliveryAttempt:
    """Parameters:
    id (required) - int64 - Event Delivery Attempt ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> EventDeliveryAttempt:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def new(*args, **kwargs) -> EventDeliveryAttempt:
    return EventDeliveryAttempt(*args, **kwargs)

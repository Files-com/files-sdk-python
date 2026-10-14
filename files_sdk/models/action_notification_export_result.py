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


class ActionNotificationExportResult:
    """A action notification export result record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Notification ID
        created_at: int64 - When the notification was sent.
        status: int64 - HTTP status code returned in the webhook response.
        message: string - A message indicating the overall status of the webhook notification.
        success: boolean - `true` if the webhook succeeded by receiving a 200 or 204 response.
        request_headers: string - A JSON-encoded string with headers that were sent with the webhook.
        request_method: string - The HTTP verb used to perform the webhook.
        request_url: string - The webhook request URL.
        path: string - The path to the actual file that triggered this notification. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        folder: string - The folder associated with the triggering action for this notification.
    """

    default_attributes = {
        "id": None,  # int64 - Notification ID
        "created_at": None,  # int64 - When the notification was sent.
        "status": None,  # int64 - HTTP status code returned in the webhook response.
        "message": None,  # string - A message indicating the overall status of the webhook notification.
        "success": None,  # boolean - `true` if the webhook succeeded by receiving a 200 or 204 response.
        "request_headers": None,  # string - A JSON-encoded string with headers that were sent with the webhook.
        "request_method": None,  # string - The HTTP verb used to perform the webhook.
        "request_url": None,  # string - The webhook request URL.
        "path": None,  # string - The path to the actual file that triggered this notification. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "folder": None,  # string - The folder associated with the triggering action for this notification.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    created_at: int | None
    status: int | None
    message: str | None
    success: bool | None
    request_headers: str | None
    request_method: str | None
    request_url: str | None
    path: str | None
    folder: str | None

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
        ) in ActionNotificationExportResult.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in ActionNotificationExportResult.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)


class ActionNotificationExportResultResource:
    """ActionNotificationExportResult operations that use one client's configuration.

    Get one from a client, such as ``client.action_notification_export_result``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ActionNotificationExportResult]:
        """Parameters:
        user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        action_notification_export_id (required) - int64 - ID of the associated action notification export.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "cursor" in params and not isinstance(params["cursor"], str):
            raise InvalidParameterError("Bad parameter: cursor must be an str")
        if "per_page" in params and (
            not isinstance(params["per_page"], int)
            or isinstance(params["per_page"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: per_page must be an int"
            )
        if "action_notification_export_id" in params and (
            not isinstance(params["action_notification_export_id"], int)
            or isinstance(params["action_notification_export_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: action_notification_export_id must be an int"
            )
        if "action_notification_export_id" not in params:
            raise MissingParameterError(
                "Parameter missing: action_notification_export_id"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            ActionNotificationExportResult,
            "GET",
            "/action_notification_export_results",
            params,
            operation,
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[ActionNotificationExportResult]:
        """The same as list()."""
        return self.list(params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ActionNotificationExportResult:
        """A new ActionNotificationExportResult with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = ActionNotificationExportResult(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = ActionNotificationExportResultResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ActionNotificationExportResult]:
    """Parameters:
    user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    action_notification_export_id (required) - int64 - ID of the associated action notification export.
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[ActionNotificationExportResult]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def new(*args, **kwargs) -> ActionNotificationExportResult:
    return ActionNotificationExportResult(*args, **kwargs)

import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class ActionNotificationExportResult:
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
        ) in ActionNotificationExportResult.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in ActionNotificationExportResult.default_attributes
            if getattr(self, k, None) is not None
        }


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   action_notification_export_id (required) - int64 - ID of the associated action notification export.
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    if "action_notification_export_id" in params and not isinstance(
        params["action_notification_export_id"], int
    ):
        raise InvalidParameterError(
            "Bad parameter: action_notification_export_id must be an int"
        )
    if "action_notification_export_id" not in params:
        raise MissingParameterError(
            "Parameter missing: action_notification_export_id"
        )
    return ListObj(
        ActionNotificationExportResult,
        "GET",
        "/action_notification_export_results",
        params,
        options,
    )


def all(params=None, options=None):
    list(params, options)


def new(*args, **kwargs):
    return ActionNotificationExportResult(*args, **kwargs)

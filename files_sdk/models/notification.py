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


class Notification:
    """A notification record from the Files.com API.

    An attribute the API did not send is None.

    Attributes:
        id: int64 - Notification ID
        path: string - Folder path to notify on. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        group_id: int64 - ID of Group to receive notifications
        group_name: string - Group name, if a Group ID is set
        group_ids: array(int64) - Group IDs when the notification requires multiple groups
        group_names: array(string) - Group names when the notification requires multiple groups
        triggering_group_ids: array(int64) - If set, will only notify on actions made by a member of one of the specified groups
        triggering_user_ids: array(int64) - If set, will only notify on actions made one of the specified users
        trigger_by_share_recipients: boolean - Notify when actions are performed by a share recipient?
        notify_user_actions: boolean - If true, will send notifications about a user's own activity to that user. If false, only activity performed by other users (or anonymous users) will be sent in notifications.
        notify_on_copy: boolean - Trigger on files copied to this path?
        notify_on_delete: boolean - Trigger on files deleted in this path?
        notify_on_download: boolean - Trigger on files downloaded in this path?
        notify_on_move: boolean - Trigger on files moved to this path?
        notify_on_upload: boolean - Trigger on files created/uploaded/updated/changed in this path?
        recursive: boolean - Apply notification recursively? This will enable notifications for each subfolder.
        send_interval: string - The time interval that notifications are aggregated to
        subject: string - Custom subject line to use for notification emails
        message: string - Custom message to include in notification emails
        triggering_filenames: array(string) - Array of filenames (possibly with wildcards) to scope trigger
        workspace_id: int64 - Workspace ID. `0` means the default workspace.
        unsubscribed: boolean - Is the user unsubscribed from this notification?
        unsubscribed_reason: string - The reason that the user unsubscribed
        user_id: int64 - Notification user ID
        username: string - Notification username
        suppressed_email: boolean - If true, it means that the recipient at this user's email address has manually unsubscribed from all emails, or had their email "hard bounce", which means that we are unable to send mail to this user's current email address. Notifications will resume if the user changes their email address.
    """

    default_attributes = {
        "id": None,  # int64 - Notification ID
        "path": None,  # string - Folder path to notify on. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "group_id": None,  # int64 - ID of Group to receive notifications
        "group_name": None,  # string - Group name, if a Group ID is set
        "group_ids": None,  # array(int64) - Group IDs when the notification requires multiple groups
        "group_names": None,  # array(string) - Group names when the notification requires multiple groups
        "triggering_group_ids": None,  # array(int64) - If set, will only notify on actions made by a member of one of the specified groups
        "triggering_user_ids": None,  # array(int64) - If set, will only notify on actions made one of the specified users
        "trigger_by_share_recipients": None,  # boolean - Notify when actions are performed by a share recipient?
        "notify_user_actions": None,  # boolean - If true, will send notifications about a user's own activity to that user.  If false, only activity performed by other users (or anonymous users) will be sent in notifications.
        "notify_on_copy": None,  # boolean - Trigger on files copied to this path?
        "notify_on_delete": None,  # boolean - Trigger on files deleted in this path?
        "notify_on_download": None,  # boolean - Trigger on files downloaded in this path?
        "notify_on_move": None,  # boolean - Trigger on files moved to this path?
        "notify_on_upload": None,  # boolean - Trigger on files created/uploaded/updated/changed in this path?
        "recursive": None,  # boolean - Apply notification recursively?  This will enable notifications for each subfolder.
        "send_interval": None,  # string - The time interval that notifications are aggregated to
        "subject": None,  # string - Custom subject line to use for notification emails
        "message": None,  # string - Custom message to include in notification emails
        "triggering_filenames": None,  # array(string) - Array of filenames (possibly with wildcards) to scope trigger
        "workspace_id": None,  # int64 - Workspace ID. `0` means the default workspace.
        "unsubscribed": None,  # boolean - Is the user unsubscribed from this notification?
        "unsubscribed_reason": None,  # string - The reason that the user unsubscribed
        "user_id": None,  # int64 - Notification user ID
        "username": None,  # string - Notification username
        "suppressed_email": None,  # boolean - If true, it means that the recipient at this user's email address has manually unsubscribed from all emails, or had their email "hard bounce", which means that we are unable to send mail to this user's current email address. Notifications will resume if the user changes their email address.
    }

    # Declared for type checkers and editors: the type the API sends each
    # attribute as, or None. set_attributes stores each value as given,
    # converting only decimals, so a value a caller sets can differ.
    id: int | None
    path: str | None
    group_id: int | None
    group_name: str | None
    group_ids: builtins.list[int] | None
    group_names: builtins.list[str] | None
    triggering_group_ids: builtins.list[int] | None
    triggering_user_ids: builtins.list[int] | None
    trigger_by_share_recipients: bool | None
    notify_user_actions: bool | None
    notify_on_copy: bool | None
    notify_on_delete: bool | None
    notify_on_download: bool | None
    notify_on_move: bool | None
    notify_on_upload: bool | None
    recursive: bool | None
    send_interval: str | None
    subject: str | None
    message: str | None
    triggering_filenames: builtins.list[str] | None
    workspace_id: int | None
    unsubscribed: bool | None
    unsubscribed_reason: str | None
    user_id: int | None
    username: str | None
    suppressed_email: bool | None

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
        ) in Notification.default_attributes.items():
            value = attributes.get(attribute, default_value)
            setattr(self, attribute, value)

    def get_attributes(self):
        attrs = {
            k: getattr(self, k, None)
            for k in Notification.default_attributes
            if getattr(self, k, None) is not None
        }
        return attrs

    def _scope(self):
        if self._context is not None:
            return self._context
        return LegacyScope(self.options)

    def update(self, params: dict[str, Any] | None = None) -> None:
        """Updates this object in place with the record the server returns, and returns None.

        Parameters:
          notify_on_copy - boolean - If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
          notify_on_delete - boolean - Trigger on files deleted in this path?
          notify_on_download - boolean - Trigger on files downloaded in this path?
          notify_on_move - boolean - Trigger on files moved to this path?
          notify_on_upload - boolean - Trigger on files created/uploaded/updated/changed in this path?
          notify_user_actions - boolean - If `true` actions initiated by the user will still result in a notification
          recursive - boolean - If `true`, enable notifications for each subfolder in this path
          send_interval - string - The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
          subject - string - Custom subject line to use for notification emails
          message - string - Custom message to include in notification emails
          triggering_filenames - array(string) - Array of filenames (possibly with wildcards) to scope trigger
          triggering_group_ids - array(int64) - If set, will only notify on actions made by a member of one of the specified groups
          triggering_user_ids - array(int64) - If set, will only notify on actions made one of the specified users
          trigger_by_share_recipients - boolean - Notify when actions are performed by a share recipient?
          workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "notify_on_copy" in params and isinstance(
            params["notify_on_copy"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_copy must be an bool"
            )
        if "notify_on_delete" in params and isinstance(
            params["notify_on_delete"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_delete must be an bool"
            )
        if "notify_on_download" in params and isinstance(
            params["notify_on_download"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_download must be an bool"
            )
        if "notify_on_move" in params and isinstance(
            params["notify_on_move"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_move must be an bool"
            )
        if "notify_on_upload" in params and isinstance(
            params["notify_on_upload"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_upload must be an bool"
            )
        if "notify_user_actions" in params and isinstance(
            params["notify_user_actions"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_user_actions must be an bool"
            )
        if "recursive" in params and isinstance(
            params["recursive"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "send_interval" in params and not isinstance(
            params["send_interval"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: send_interval must be an str"
            )
        if "subject" in params and not isinstance(params["subject"], str):
            raise InvalidParameterError(
                "Bad parameter: subject must be an str"
            )
        if "message" in params and not isinstance(params["message"], str):
            raise InvalidParameterError(
                "Bad parameter: message must be an str"
            )
        if "triggering_filenames" in params and not isinstance(
            params["triggering_filenames"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_filenames must be an list"
            )
        if "triggering_group_ids" in params and not isinstance(
            params["triggering_group_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_group_ids must be an list"
            )
        if "triggering_user_ids" in params and not isinstance(
            params["triggering_user_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_user_ids must be an list"
            )
        if "trigger_by_share_recipients" in params and isinstance(
            params["trigger_by_share_recipients"], (builtins.list, tuple, dict)
        ):
            raise InvalidParameterError(
                "Bad parameter: trigger_by_share_recipients must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        operation = Operation.start(self._scope())
        response = operation.request(
            "PATCH", "/notifications/" + path_value(params["id"]), params
        )
        decode_record(response, response.data, self.set_attributes)
        operation.adopt(self)

    def delete(self, params: dict[str, Any] | None = None) -> None:
        if not (hasattr(self, "id") and self.id):
            raise MissingParameterError("Current object doesn't have a id")
        params = copy_params(params, {"id": self.id})
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        operation = Operation.start(self._scope())
        operation.request(
            "DELETE", "/notifications/" + path_value(params["id"]), params
        )

    def destroy(self, params: dict[str, Any] | None = None) -> None:
        """The same as delete()."""
        return self.delete(params)

    def save(self) -> None:
        """Update this object on the server if it has an id, or else create
        it, taking in place the record the server returns."""
        if hasattr(self, "id") and self.id:
            self.update(self.get_attributes())
        else:
            new_obj = NotificationResource(self._scope()).create(
                self.get_attributes()
            )
            self.set_attributes(new_obj.get_attributes())
            self._context = new_obj._context


class NotificationResource:
    """Notification operations that use one client's configuration.

    Get one from a client, such as ``client.notification``. Each operation
    takes the same arguments as the module-level function of the same name,
    and its options apply on top of the client's.
    """

    def __init__(self, scope):
        self._scope = scope

    def list(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Notification]:
        """Parameters:
        cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
        per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
        sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `path`, `user_id` or `group_id`.
        filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `user_id`, `workspace_id` or `group_id`. Valid field combinations are `[ workspace_id, path ]`, `[ workspace_id, user_id ]`, `[ workspace_id, group_id ]` or `[ workspace_id, user_id, path ]`.
        filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
        path - string - Show notifications for this Path.
        include_ancestors - boolean - If `include_ancestors` is `true` and `path` is specified, include notifications for any parent paths. Ignored if `path` is not specified.
        group_id - string
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
        if "filter_prefix" in params and not isinstance(
            params["filter_prefix"], dict
        ):
            raise InvalidParameterError(
                "Bad parameter: filter_prefix must be an dict"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "include_ancestors" in params and not isinstance(
            params["include_ancestors"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: include_ancestors must be an bool"
            )
        if "group_id" in params and not isinstance(params["group_id"], str):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an str"
            )
        operation = Operation.start(self._scope, options)
        return ListObj(
            Notification, "GET", "/notifications", params, operation
        )

    def all(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> ListObj[Notification]:
        """The same as list()."""
        return self.list(params, options)

    def find(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Notification:
        """Parameters:
        id (required) - int64 - Notification ID.
        """
        return self.__find({"id": id}, params, options)

    def __find(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Notification:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "GET", "/notifications/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Notification)

    def get(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Notification:
        """The same as find()."""
        return self.find(id, params, options)

    def create(
        self,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Notification:
        """Parameters:
        user_id - int64 - The id of the user to notify. Provide `user_id`, `username` or `group_id`.
        notify_on_copy - boolean - If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
        notify_on_delete - boolean - Trigger on files deleted in this path?
        notify_on_download - boolean - Trigger on files downloaded in this path?
        notify_on_move - boolean - Trigger on files moved to this path?
        notify_on_upload - boolean - Trigger on files created/uploaded/updated/changed in this path?
        notify_user_actions - boolean - If `true` actions initiated by the user will still result in a notification
        recursive - boolean - If `true`, enable notifications for each subfolder in this path
        send_interval - string - The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
        subject - string - Custom subject line to use for notification emails
        message - string - Custom message to include in notification emails
        triggering_filenames - array(string) - Array of filenames (possibly with wildcards) to scope trigger
        triggering_group_ids - array(int64) - If set, will only notify on actions made by a member of one of the specified groups
        triggering_user_ids - array(int64) - If set, will only notify on actions made one of the specified users
        trigger_by_share_recipients - boolean - Notify when actions are performed by a share recipient?
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        group_id - int64 - The ID of the group to notify.  Provide `user_id`, `username` or `group_id`.
        group_ids - string - Group IDs when the notification requires multiple groups. If sent as a string, it should be comma-delimited.
        path - string - Path
        username - string - The username of the user to notify.  Provide `user_id`, `username` or `group_id`.
        """
        params = copy_params(params)
        if "user_id" in params and (
            not isinstance(params["user_id"], int)
            or isinstance(params["user_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: user_id must be an int"
            )
        if "notify_on_copy" in params and not isinstance(
            params["notify_on_copy"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_copy must be an bool"
            )
        if "notify_on_delete" in params and not isinstance(
            params["notify_on_delete"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_delete must be an bool"
            )
        if "notify_on_download" in params and not isinstance(
            params["notify_on_download"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_download must be an bool"
            )
        if "notify_on_move" in params and not isinstance(
            params["notify_on_move"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_move must be an bool"
            )
        if "notify_on_upload" in params and not isinstance(
            params["notify_on_upload"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_upload must be an bool"
            )
        if "notify_user_actions" in params and not isinstance(
            params["notify_user_actions"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_user_actions must be an bool"
            )
        if "recursive" in params and not isinstance(params["recursive"], bool):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "send_interval" in params and not isinstance(
            params["send_interval"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: send_interval must be an str"
            )
        if "subject" in params and not isinstance(params["subject"], str):
            raise InvalidParameterError(
                "Bad parameter: subject must be an str"
            )
        if "message" in params and not isinstance(params["message"], str):
            raise InvalidParameterError(
                "Bad parameter: message must be an str"
            )
        if "triggering_filenames" in params and not isinstance(
            params["triggering_filenames"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_filenames must be an list"
            )
        if "triggering_group_ids" in params and not isinstance(
            params["triggering_group_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_group_ids must be an list"
            )
        if "triggering_user_ids" in params and not isinstance(
            params["triggering_user_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_user_ids must be an list"
            )
        if "trigger_by_share_recipients" in params and not isinstance(
            params["trigger_by_share_recipients"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: trigger_by_share_recipients must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "group_id" in params and (
            not isinstance(params["group_id"], int)
            or isinstance(params["group_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: group_id must be an int"
            )
        if "group_ids" in params and not isinstance(params["group_ids"], str):
            raise InvalidParameterError(
                "Bad parameter: group_ids must be an str"
            )
        if "path" in params and not isinstance(params["path"], str):
            raise InvalidParameterError("Bad parameter: path must be an str")
        if "username" in params and not isinstance(params["username"], str):
            raise InvalidParameterError(
                "Bad parameter: username must be an str"
            )
        operation = Operation.start(self._scope, options)
        response = operation.request("POST", "/notifications", params)
        return operation.decode_model(response, Notification)

    def update(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Notification:
        """Parameters:
        notify_on_copy - boolean - If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
        notify_on_delete - boolean - Trigger on files deleted in this path?
        notify_on_download - boolean - Trigger on files downloaded in this path?
        notify_on_move - boolean - Trigger on files moved to this path?
        notify_on_upload - boolean - Trigger on files created/uploaded/updated/changed in this path?
        notify_user_actions - boolean - If `true` actions initiated by the user will still result in a notification
        recursive - boolean - If `true`, enable notifications for each subfolder in this path
        send_interval - string - The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
        subject - string - Custom subject line to use for notification emails
        message - string - Custom message to include in notification emails
        triggering_filenames - array(string) - Array of filenames (possibly with wildcards) to scope trigger
        triggering_group_ids - array(int64) - If set, will only notify on actions made by a member of one of the specified groups
        triggering_user_ids - array(int64) - If set, will only notify on actions made one of the specified users
        trigger_by_share_recipients - boolean - Notify when actions are performed by a share recipient?
        workspace_id - int64 - Workspace ID. `0` means the default workspace.
        """
        return self.__update({"id": id}, params, options)

    def __update(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> Notification:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "notify_on_copy" in params and not isinstance(
            params["notify_on_copy"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_copy must be an bool"
            )
        if "notify_on_delete" in params and not isinstance(
            params["notify_on_delete"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_delete must be an bool"
            )
        if "notify_on_download" in params and not isinstance(
            params["notify_on_download"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_download must be an bool"
            )
        if "notify_on_move" in params and not isinstance(
            params["notify_on_move"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_move must be an bool"
            )
        if "notify_on_upload" in params and not isinstance(
            params["notify_on_upload"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_on_upload must be an bool"
            )
        if "notify_user_actions" in params and not isinstance(
            params["notify_user_actions"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: notify_user_actions must be an bool"
            )
        if "recursive" in params and not isinstance(params["recursive"], bool):
            raise InvalidParameterError(
                "Bad parameter: recursive must be an bool"
            )
        if "send_interval" in params and not isinstance(
            params["send_interval"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: send_interval must be an str"
            )
        if "subject" in params and not isinstance(params["subject"], str):
            raise InvalidParameterError(
                "Bad parameter: subject must be an str"
            )
        if "message" in params and not isinstance(params["message"], str):
            raise InvalidParameterError(
                "Bad parameter: message must be an str"
            )
        if "triggering_filenames" in params and not isinstance(
            params["triggering_filenames"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_filenames must be an list"
            )
        if "triggering_group_ids" in params and not isinstance(
            params["triggering_group_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_group_ids must be an list"
            )
        if "triggering_user_ids" in params and not isinstance(
            params["triggering_user_ids"], builtins.list
        ):
            raise InvalidParameterError(
                "Bad parameter: triggering_user_ids must be an list"
            )
        if "trigger_by_share_recipients" in params and not isinstance(
            params["trigger_by_share_recipients"], bool
        ):
            raise InvalidParameterError(
                "Bad parameter: trigger_by_share_recipients must be an bool"
            )
        if "workspace_id" in params and (
            not isinstance(params["workspace_id"], int)
            or isinstance(params["workspace_id"], bool)
        ):
            raise InvalidParameterError(
                "Bad parameter: workspace_id must be an int"
            )
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        response = operation.request(
            "PATCH", "/notifications/" + path_value(params["id"]), params
        )
        return operation.decode_model(response, Notification)

    def delete(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        return self.__delete({"id": id}, params, options)

    def __delete(
        self,
        path_values: dict[str, Any],
        params: dict[str, Any] | None,
        options: RequestOptions | Mapping[str, Any] | None,
    ) -> None:
        params = copy_params(params, path_values)
        if "id" in params and (
            not isinstance(params["id"], int) or isinstance(params["id"], bool)
        ):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        operation = Operation.start(self._scope, options)
        operation.request(
            "DELETE", "/notifications/" + path_value(params["id"]), params
        )

    def destroy(
        self,
        id: int,
        params: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> None:
        """The same as delete()."""
        return self.delete(id, params, options)

    def new(
        self,
        attributes: dict[str, Any] | None = None,
        options: RequestOptions | Mapping[str, Any] | None = None,
    ) -> Notification:
        """A new Notification with attributes, not yet saved, whose
        operations use this resource's client."""
        obj = Notification(attributes, options)
        obj._context = self._scope._context_for(options)
        return obj


_legacy_resource = NotificationResource(LEGACY)


def list(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Notification]:
    """Parameters:
    cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
    per_page - int64 - Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
    sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `path`, `user_id` or `group_id`.
    filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `user_id`, `workspace_id` or `group_id`. Valid field combinations are `[ workspace_id, path ]`, `[ workspace_id, user_id ]`, `[ workspace_id, group_id ]` or `[ workspace_id, user_id, path ]`.
    filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
    path - string - Show notifications for this Path.
    include_ancestors - boolean - If `include_ancestors` is `true` and `path` is specified, include notifications for any parent paths. Ignored if `path` is not specified.
    group_id - string
    """
    return _legacy_resource.list(params, options)


def all(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> ListObj[Notification]:
    """The same as list()."""
    return _legacy_resource.list(params, options)


def find(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Notification:
    """Parameters:
    id (required) - int64 - Notification ID.
    """
    return _legacy_resource.find(id, params, options)


def get(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Notification:
    """The same as find()."""
    return _legacy_resource.find(id, params, options)


def create(
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Notification:
    """Parameters:
    user_id - int64 - The id of the user to notify. Provide `user_id`, `username` or `group_id`.
    notify_on_copy - boolean - If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
    notify_on_delete - boolean - Trigger on files deleted in this path?
    notify_on_download - boolean - Trigger on files downloaded in this path?
    notify_on_move - boolean - Trigger on files moved to this path?
    notify_on_upload - boolean - Trigger on files created/uploaded/updated/changed in this path?
    notify_user_actions - boolean - If `true` actions initiated by the user will still result in a notification
    recursive - boolean - If `true`, enable notifications for each subfolder in this path
    send_interval - string - The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
    subject - string - Custom subject line to use for notification emails
    message - string - Custom message to include in notification emails
    triggering_filenames - array(string) - Array of filenames (possibly with wildcards) to scope trigger
    triggering_group_ids - array(int64) - If set, will only notify on actions made by a member of one of the specified groups
    triggering_user_ids - array(int64) - If set, will only notify on actions made one of the specified users
    trigger_by_share_recipients - boolean - Notify when actions are performed by a share recipient?
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
    group_id - int64 - The ID of the group to notify.  Provide `user_id`, `username` or `group_id`.
    group_ids - string - Group IDs when the notification requires multiple groups. If sent as a string, it should be comma-delimited.
    path - string - Path
    username - string - The username of the user to notify.  Provide `user_id`, `username` or `group_id`.
    """
    return _legacy_resource.create(params, options)


def update(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> Notification:
    """Parameters:
    notify_on_copy - boolean - If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
    notify_on_delete - boolean - Trigger on files deleted in this path?
    notify_on_download - boolean - Trigger on files downloaded in this path?
    notify_on_move - boolean - Trigger on files moved to this path?
    notify_on_upload - boolean - Trigger on files created/uploaded/updated/changed in this path?
    notify_user_actions - boolean - If `true` actions initiated by the user will still result in a notification
    recursive - boolean - If `true`, enable notifications for each subfolder in this path
    send_interval - string - The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
    subject - string - Custom subject line to use for notification emails
    message - string - Custom message to include in notification emails
    triggering_filenames - array(string) - Array of filenames (possibly with wildcards) to scope trigger
    triggering_group_ids - array(int64) - If set, will only notify on actions made by a member of one of the specified groups
    triggering_user_ids - array(int64) - If set, will only notify on actions made one of the specified users
    trigger_by_share_recipients - boolean - Notify when actions are performed by a share recipient?
    workspace_id - int64 - Workspace ID. `0` means the default workspace.
    """
    return _legacy_resource.update(id, params, options)


def delete(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    _legacy_resource.delete(id, params, options)


def destroy(
    id: int,
    params: dict[str, Any] | None = None,
    options: RequestOptions | Mapping[str, Any] | None = None,
) -> None:
    """The same as delete()."""
    return _legacy_resource.delete(id, params, options)


def new(*args, **kwargs) -> Notification:
    return Notification(*args, **kwargs)

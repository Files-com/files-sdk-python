import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Notification:
    default_attributes = {
        "id": None,  # int64 - Notification ID
        "path": None,  # string - Folder path to notify on This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        "group_id": None,  # int64 - ID of Group to receive notifications
        "group_name": None,  # string - Group name, if a Group ID is set
        "triggering_group_ids": None,  # array - If set, will only notify on actions made by a member of one of the specified groups
        "triggering_user_ids": None,  # array - If set, will onlynotify on actions made one of the specified users
        "trigger_by_share_recipients": None,  # boolean - Notify when actions are performed by a share recipient?
        "notify_user_actions": None,  # boolean - If true, will send notifications about a user's own activity to that user.  If false, only activity performed by other users (or anonymous users) will be sent in notifications.
        "notify_on_copy": None,  # boolean - Trigger on files copied to this path?
        "notify_on_delete": None,  # boolean - Trigger on files deleted in this path?
        "notify_on_download": None,  # boolean - Trigger on files downloaded in this path?
        "notify_on_move": None,  # boolean - Trigger on files moved to this path?
        "notify_on_upload": None,  # boolean - Trigger on files created/uploaded/updated/changed in this path?
        "recursive": None,  # boolean - Apply notification recursively?  This will enable notifications for each subfolder.
        "send_interval": None,  # string - The time interval that notifications are aggregated to
        "message": None,  # string - Custom message to include in notification emails
        "triggering_filenames": None,  # array - Array of filenames (possibly with wildcards) to scope trigger
        "unsubscribed": None,  # boolean - Is the user unsubscribed from this notification?
        "unsubscribed_reason": None,  # string - The reason that the user unsubscribed
        "user_id": None,  # int64 - Notification user ID
        "username": None,  # string - Notification username
        "suppressed_email": None,  # boolean - If true, it means that the recipient at this user's email address has manually unsubscribed from all emails, or had their email "hard bounce", which means that we are unable to send mail to this user's current email address. Notifications will resume if the user changes their email address.
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
        ) in Notification.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Notification.default_attributes
            if getattr(self, k, None) is not None
        }

    # Parameters:
    #   notify_on_copy - boolean - If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
    #   notify_on_delete - boolean - Trigger on files deleted in this path?
    #   notify_on_download - boolean - Trigger on files downloaded in this path?
    #   notify_on_move - boolean - Trigger on files moved to this path?
    #   notify_on_upload - boolean - Trigger on files created/uploaded/updated/changed in this path?
    #   notify_user_actions - boolean - If `true` actions initiated by the user will still result in a notification
    #   recursive - boolean - If `true`, enable notifications for each subfolder in this path
    #   send_interval - string - The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
    #   message - string - Custom message to include in notification emails
    #   triggering_filenames - array(string) - Array of filenames (possibly with wildcards) to scope trigger
    #   triggering_group_ids - array(int64) - If set, will only notify on actions made by a member of one of the specified groups
    #   triggering_user_ids - array(int64) - If set, will onlynotify on actions made one of the specified users
    #   trigger_by_share_recipients - boolean - Notify when actions are performed by a share recipient?
    def update(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        if "send_interval" in params and not isinstance(
            params["send_interval"], str
        ):
            raise InvalidParameterError(
                "Bad parameter: send_interval must be an str"
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
        response, _options = Api.send_request(
            "PATCH",
            "/notifications/{id}".format(id=params["id"]),
            params,
            self.options,
        )
        return response.data

    def delete(self, params=None):
        if not isinstance(params, dict):
            params = {}

        if hasattr(self, "id") and self.id:
            params["id"] = self.id
        else:
            raise MissingParameterError("Current object doesn't have a id")
        if "id" not in params:
            raise MissingParameterError("Parameter missing: id")
        if "id" in params and not isinstance(params["id"], int):
            raise InvalidParameterError("Bad parameter: id must be an int")
        Api.send_request(
            "DELETE",
            "/notifications/{id}".format(id=params["id"]),
            params,
            self.options,
        )

    def destroy(self, params=None):
        self.delete(params)

    def save(self):
        if hasattr(self, "id") and self.id:
            new_obj = self.update(self.get_attributes())
            self.set_attributes(new_obj.get_attributes())
            return True
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   user_id - int64 - DEPRECATED: Show notifications for this User ID. Use `filter[user_id]` instead.
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   sort_by - object - If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[path]=desc`). Valid fields are `path`, `user_id` or `group_id`.
#   filter - object - If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `user_id` or `group_id`.
#   filter_prefix - object - If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
#   path - string - Show notifications for this Path.
#   include_ancestors - boolean - If `include_ancestors` is `true` and `path` is specified, include notifications for any parent paths. Ignored if `path` is not specified.
#   group_id - string
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
    if "sort_by" in params and not isinstance(params["sort_by"], dict):
        raise InvalidParameterError("Bad parameter: sort_by must be an dict")
    if "filter" in params and not isinstance(params["filter"], dict):
        raise InvalidParameterError("Bad parameter: filter must be an dict")
    if "filter_prefix" in params and not isinstance(
        params["filter_prefix"], dict
    ):
        raise InvalidParameterError(
            "Bad parameter: filter_prefix must be an dict"
        )
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "group_id" in params and not isinstance(params["group_id"], str):
        raise InvalidParameterError("Bad parameter: group_id must be an str")
    return ListObj(Notification, "GET", "/notifications", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   id (required) - int64 - Notification ID.
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
        "GET", "/notifications/{id}".format(id=params["id"]), params, options
    )
    return Notification(response.data, options)


def get(id, params=None, options=None):
    find(id, params, options)


# Parameters:
#   user_id - int64 - The id of the user to notify. Provide `user_id`, `username` or `group_id`.
#   notify_on_copy - boolean - If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
#   notify_on_delete - boolean - Trigger on files deleted in this path?
#   notify_on_download - boolean - Trigger on files downloaded in this path?
#   notify_on_move - boolean - Trigger on files moved to this path?
#   notify_on_upload - boolean - Trigger on files created/uploaded/updated/changed in this path?
#   notify_user_actions - boolean - If `true` actions initiated by the user will still result in a notification
#   recursive - boolean - If `true`, enable notifications for each subfolder in this path
#   send_interval - string - The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
#   message - string - Custom message to include in notification emails
#   triggering_filenames - array(string) - Array of filenames (possibly with wildcards) to scope trigger
#   triggering_group_ids - array(int64) - If set, will only notify on actions made by a member of one of the specified groups
#   triggering_user_ids - array(int64) - If set, will onlynotify on actions made one of the specified users
#   trigger_by_share_recipients - boolean - Notify when actions are performed by a share recipient?
#   group_id - int64 - The ID of the group to notify.  Provide `user_id`, `username` or `group_id`.
#   path - string - Path
#   username - string - The username of the user to notify.  Provide `user_id`, `username` or `group_id`.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "user_id" in params and not isinstance(params["user_id"], int):
        raise InvalidParameterError("Bad parameter: user_id must be an int")
    if "send_interval" in params and not isinstance(
        params["send_interval"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: send_interval must be an str"
        )
    if "message" in params and not isinstance(params["message"], str):
        raise InvalidParameterError("Bad parameter: message must be an str")
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
    if "group_id" in params and not isinstance(params["group_id"], int):
        raise InvalidParameterError("Bad parameter: group_id must be an int")
    if "path" in params and not isinstance(params["path"], str):
        raise InvalidParameterError("Bad parameter: path must be an str")
    if "username" in params and not isinstance(params["username"], str):
        raise InvalidParameterError("Bad parameter: username must be an str")
    response, options = Api.send_request(
        "POST", "/notifications", params, options
    )
    return Notification(response.data, options)


# Parameters:
#   notify_on_copy - boolean - If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
#   notify_on_delete - boolean - Trigger on files deleted in this path?
#   notify_on_download - boolean - Trigger on files downloaded in this path?
#   notify_on_move - boolean - Trigger on files moved to this path?
#   notify_on_upload - boolean - Trigger on files created/uploaded/updated/changed in this path?
#   notify_user_actions - boolean - If `true` actions initiated by the user will still result in a notification
#   recursive - boolean - If `true`, enable notifications for each subfolder in this path
#   send_interval - string - The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
#   message - string - Custom message to include in notification emails
#   triggering_filenames - array(string) - Array of filenames (possibly with wildcards) to scope trigger
#   triggering_group_ids - array(int64) - If set, will only notify on actions made by a member of one of the specified groups
#   triggering_user_ids - array(int64) - If set, will onlynotify on actions made one of the specified users
#   trigger_by_share_recipients - boolean - Notify when actions are performed by a share recipient?
def update(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "send_interval" in params and not isinstance(
        params["send_interval"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: send_interval must be an str"
        )
    if "message" in params and not isinstance(params["message"], str):
        raise InvalidParameterError("Bad parameter: message must be an str")
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
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    response, options = Api.send_request(
        "PATCH", "/notifications/{id}".format(id=params["id"]), params, options
    )
    return Notification(response.data, options)


def delete(id, params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    params["id"] = id
    if "id" in params and not isinstance(params["id"], int):
        raise InvalidParameterError("Bad parameter: id must be an int")
    if "id" not in params:
        raise MissingParameterError("Parameter missing: id")
    Api.send_request(
        "DELETE",
        "/notifications/{id}".format(id=params["id"]),
        params,
        options,
    )


def destroy(id, params=None, options=None):
    delete(id, params, options)


def new(*args, **kwargs):
    return Notification(*args, **kwargs)

import builtins  # noqa: F401
from files_sdk.api import Api  # noqa: F401
from files_sdk.list_obj import ListObj
from files_sdk.error import (  # noqa: F401
    InvalidParameterError,
    MissingParameterError,
    NotImplementedError,
)


class Restore:
    default_attributes = {
        "earliest_date": None,  # date-time - Restore all files deleted after this date/time. Don't set this earlier than you need. Can not be greater than 365 days prior to the restore request.
        "id": None,  # int64 - Restore Record ID.
        "dirs_restored": None,  # int64 - Number of directories that were successfully restored.
        "dirs_errored": None,  # int64 - Number of directories that were not able to be restored.
        "dirs_total": None,  # int64 - Total number of directories processed.
        "files_restored": None,  # int64 - Number of files successfully restored.
        "files_errored": None,  # int64 - Number of files that were not able to be restored.
        "files_total": None,  # int64 - Total number of files processed.
        "prefix": None,  # string - Prefix of the files/folders to restore. To restore a folder, add a trailing slash to the folder name. Do not use a leading slash. To restore all deleted items, specify an empty string (`''`) in the prefix field or omit the field from the request.
        "restore_in_place": None,  # boolean - If true, we will restore the files in place (into their original paths). If false, we will create a new restoration folder in the root and restore files there.
        "restore_deleted_permissions": None,  # boolean - If true, we will also restore any Permissions that match the same path prefix from the same dates.
        "status": None,  # string - Status of the restoration process.
        "update_timestamps": None,  # boolean - If true, we will update the last modified timestamp of restored files to today's date. If false, we might trigger File Expiration to delete the file again.
        "error_messages": None,  # array(string) - Error messages received while restoring files and/or directories. Only present if there were errors.
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for attribute, default_value in Restore.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {
            k: getattr(self, k, None)
            for k in Restore.default_attributes
            if getattr(self, k, None) is not None
        }

    def save(self):
        if hasattr(self, "id") and self.id:
            raise NotImplementedError(
                "The Restore object doesn't support updates."
            )
        else:
            new_obj = create(self.get_attributes(), self.options)
            self.set_attributes(new_obj.get_attributes())
            return True


# Parameters:
#   cursor - string - Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
def list(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "cursor" in params and not isinstance(params["cursor"], str):
        raise InvalidParameterError("Bad parameter: cursor must be an str")
    if "per_page" in params and not isinstance(params["per_page"], int):
        raise InvalidParameterError("Bad parameter: per_page must be an int")
    return ListObj(Restore, "GET", "/restores", params, options)


def all(params=None, options=None):
    list(params, options)


# Parameters:
#   earliest_date (required) - string - Restore all files deleted after this date/time. Don't set this earlier than you need. Can not be greater than 365 days prior to the restore request.
#   prefix - string - Prefix of the files/folders to restore. To restore a folder, add a trailing slash to the folder name. Do not use a leading slash. To restore all deleted items, specify an empty string (`''`) in the prefix field or omit the field from the request.
#   restore_deleted_permissions - boolean - If true, we will also restore any Permissions that match the same path prefix from the same dates.
#   restore_in_place - boolean - If true, we will restore the files in place (into their original paths). If false, we will create a new restoration folder in the root and restore files there.
#   update_timestamps - boolean - If true, we will update the last modified timestamp of restored files to today's date. If false, we might trigger File Expiration to delete the file again.
def create(params=None, options=None):
    if not isinstance(params, dict):
        params = {}
    if not isinstance(options, dict):
        options = {}
    if "earliest_date" in params and not isinstance(
        params["earliest_date"], str
    ):
        raise InvalidParameterError(
            "Bad parameter: earliest_date must be an str"
        )
    if "prefix" in params and not isinstance(params["prefix"], str):
        raise InvalidParameterError("Bad parameter: prefix must be an str")
    if "earliest_date" not in params:
        raise MissingParameterError("Parameter missing: earliest_date")
    response, options = Api.send_request("POST", "/restores", params, options)
    return Restore(response.data, options)


def new(*args, **kwargs):
    return Restore(*args, **kwargs)

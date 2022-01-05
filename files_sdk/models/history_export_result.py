import builtins
import datetime
from files_sdk.api import Api
from files_sdk.list_obj import ListObj
from files_sdk.exceptions import InvalidParameterError, MissingParameterError, NotImplementedError

class HistoryExportResult:
    default_attributes = {
        'id': None,     # int64 - Action ID
        'created_at': None,     # int64 - When the action happened
        'user_id': None,     # int64 - User ID
        'file_id': None,     # int64 - File ID related to the action
        'parent_id': None,     # int64 - ID of the parent folder
        'path': None,     # string - Path of the related action This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
        'folder': None,     # string - Folder in which the action occurred
        'src': None,     # string - File move originated from this path
        'destination': None,     # string - File moved to this destination folder
        'ip': None,     # string - Client IP that performed the action
        'username': None,     # string - Username of the user that performed the action
        'action': None,     # string - What action was taken. Valid values: `create`, `read`, `update`, `destroy`, `move`, `login`, `failedlogin`, `copy`, `user_create`, `user_update`, `user_destroy`, `group_create`, `group_update`, `group_destroy`, `permission_create`, `permission_destroy`, `api_key_create`, `api_key_update`, `api_key_destroy`
        'failure_type': None,     # string - The type of login failure, if applicable.  Valid values: `expired_trial`, `account_overdue`, `locked_out`, `ip_mismatch`, `password_mismatch`, `site_mismatch`, `username_not_found`, `none`, `no_ftp_permission`, `no_web_permission`, `no_directory`, `errno_enoent`, `no_sftp_permission`, `no_dav_permission`, `no_restapi_permission`, `key_mismatch`, `region_mismatch`, `expired_access`, `desktop_ip_mismatch`, `desktop_api_key_not_used_quickly_enough`, `disabled`, `country_mismatch`
        'interface': None,     # string - Inteface through which the action was taken. Valid values: `web`, `ftp`, `robot`, `jsapi`, `webdesktopapi`, `sftp`, `dav`, `desktop`, `restapi`, `scim`, `office`, `mobile`, `as2`
        'target_id': None,     # int64 - ID of the object (such as Users, or API Keys) on which the action was taken
        'target_name': None,     # string - Name of the User, Group or other object with a name related to this action
        'target_permission': None,     # string - Permission level of the action
        'target_recursive': None,     # boolean - Whether or not the action was recursive
        'target_expires_at': None,     # int64 - If searching for Histories about API keys, this is when the API key will expire
        'target_permission_set': None,     # string - If searching for Histories about API keys, this represents the permission set of the associated  API key
        'target_platform': None,     # string - If searching for Histories about API keys, this is the platform on which the action was taken
        'target_username': None,     # string - If searching for Histories about API keys, this is the username on which the action was taken
        'target_user_id': None,     # int64 - If searching for Histories about API keys, this is the User ID on which the action was taken
    }

    def __init__(self, attributes=None, options=None):
        if not isinstance(attributes, dict):
            attributes = {}
        if not isinstance(options, dict):
            options = {}
        self.set_attributes(attributes)
        self.options = options

    def set_attributes(self, attributes):
        for (attribute, default_value) in HistoryExportResult.default_attributes.items():
            setattr(self, attribute, attributes.get(attribute, default_value))

    def get_attributes(self):
        return {k: getattr(self, k, None) for k in HistoryExportResult.default_attributes if getattr(self, k, None) is not None}


# Parameters:
#   user_id - int64 - User ID.  Provide a value of `0` to operate the current session's user.
#   cursor - string - Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
#   per_page - int64 - Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
#   history_export_id (required) - int64 - ID of the associated history export.
def list(params = None, options = None):
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
    if "history_export_id" in params and not isinstance(params["history_export_id"], int):
        raise InvalidParameterError("Bad parameter: history_export_id must be an int")
    if "history_export_id" not in params:
        raise MissingParameterError("Parameter missing: history_export_id")
    return ListObj(HistoryExportResult,"GET", "/history_export_results", params, options)

def all(params = None, options = None):
    list(params, options)

def new(*args, **kwargs):
    return HistoryExportResult(*args, **kwargs)
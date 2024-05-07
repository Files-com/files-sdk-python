# HistoryExportResult

## Example HistoryExportResult Object

```
{
  "id": 1,
  "created_at": 1,
  "created_at_iso8601": "example",
  "user_id": 1,
  "file_id": 1,
  "parent_id": 1,
  "path": "MyFile.txt",
  "folder": "Folder",
  "src": "SrcFolder",
  "destination": "DestFolder",
  "ip": "127.0.0.1",
  "username": "jerry",
  "action": "read",
  "failure_type": "bad_password",
  "interface": "ftp",
  "target_id": 1,
  "target_name": "full",
  "target_permission": "full",
  "target_recursive": True,
  "target_expires_at": 1,
  "target_expires_at_iso8601": "example",
  "target_permission_set": "desktop_app",
  "target_platform": "windows",
  "target_username": "jerry",
  "target_user_id": 1
}
```

* `id` (int64): Action ID
* `created_at` (int64): When the action happened
* `created_at_iso8601` (string): When the action happened, in ISO8601 format.
* `user_id` (int64): User ID
* `file_id` (int64): File ID related to the action
* `parent_id` (int64): ID of the parent folder
* `path` (string): Path of the related action This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `folder` (string): Folder in which the action occurred
* `src` (string): File move originated from this path
* `destination` (string): File moved to this destination folder
* `ip` (string): Client IP that performed the action
* `username` (string): Username of the user that performed the action
* `action` (string): What action was taken. Valid values: `create`, `read`, `update`, `destroy`, `move`, `login`, `failedlogin`, `copy`, `user_create`, `user_update`, `user_destroy`, `group_create`, `group_update`, `group_destroy`, `permission_create`, `permission_destroy`, `api_key_create`, `api_key_update`, `api_key_destroy`
* `failure_type` (string): The type of login failure, if applicable.  Valid values: `expired_trial`, `account_overdue`, `locked_out`, `ip_mismatch`, `password_mismatch`, `site_mismatch`, `username_not_found`, `none`, `no_ftp_permission`, `no_web_permission`, `no_directory`, `errno_enoent`, `no_sftp_permission`, `no_dav_permission`, `no_restapi_permission`, `key_mismatch`, `region_mismatch`, `expired_access`, `desktop_ip_mismatch`, `desktop_api_key_not_used_quickly_enough`, `disabled`, `country_mismatch`, `insecure_ftp`, `insecure_cipher`, `rate_limited`
* `interface` (string): Inteface through which the action was taken. Valid values: `web`, `ftp`, `robot`, `jsapi`, `webdesktopapi`, `sftp`, `dav`, `desktop`, `restapi`, `scim`, `office`, `mobile`, `as2`, `inbound_email`, `remote`
* `target_id` (int64): ID of the object (such as Users, or API Keys) on which the action was taken
* `target_name` (string): Name of the User, Group or other object with a name related to this action
* `target_permission` (string): Permission level of the action
* `target_recursive` (boolean): Whether or not the action was recursive
* `target_expires_at` (int64): If searching for Histories about API keys, this is when the API key will expire. Represented as a Unix timestamp.
* `target_expires_at_iso8601` (string): If searching for Histories about API keys, this is when the API key will expire. Represented in ISO8601 format.
* `target_permission_set` (string): If searching for Histories about API keys, this represents the permission set of the associated  API key
* `target_platform` (string): If searching for Histories about API keys, this is the platform on which the action was taken
* `target_username` (string): If searching for Histories about API keys, this is the username on which the action was taken
* `target_user_id` (int64): If searching for Histories about API keys, this is the User ID on which the action was taken


---

## List History Export Results

```
files_sdk.history_export_result.list({
  "user_id": 1,
  "per_page": 1,
  "history_export_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `history_export_id` (int64): Required - ID of the associated history export.

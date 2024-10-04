# HistoryExport

## Example HistoryExport Object

```
{
  "id": 1,
  "history_version": "example",
  "start_at": "2000-01-01T01:00:00Z",
  "end_at": "2000-01-01T01:00:00Z",
  "status": "ready",
  "query_action": "read",
  "query_interface": "ftp",
  "query_user_id": "1",
  "query_file_id": "1",
  "query_parent_id": "1",
  "query_path": "MyFile.txt",
  "query_folder": "Folder",
  "query_src": "SrcFolder",
  "query_destination": "DestFolder",
  "query_ip": "127.0.0.1",
  "query_username": "jerry",
  "query_failure_type": "bad_password",
  "query_target_id": "1",
  "query_target_name": "full",
  "query_target_permission": "full",
  "query_target_user_id": "1",
  "query_target_username": "jerry",
  "query_target_platform": "windows",
  "query_target_permission_set": "desktop_app",
  "results_url": "https://files.com/history_results.csv"
}
```

* `id` (int64): History Export ID
* `history_version` (string): Version of the history for the export.
* `start_at` (date-time): Start date/time of export range.
* `end_at` (date-time): End date/time of export range.
* `status` (string): Status of export.  Will be: `building`, `ready`, or `failed`
* `query_action` (string): Filter results by this this action type. Valid values: `create`, `read`, `update`, `destroy`, `move`, `login`, `failedlogin`, `copy`, `user_create`, `user_update`, `user_destroy`, `group_create`, `group_update`, `group_destroy`, `permission_create`, `permission_destroy`, `api_key_create`, `api_key_update`, `api_key_destroy`
* `query_interface` (string): Filter results by this this interface type. Valid values: `web`, `ftp`, `robot`, `jsapi`, `webdesktopapi`, `sftp`, `dav`, `desktop`, `restapi`, `scim`, `office`, `mobile`, `as2`, `inbound_email`, `remote`
* `query_user_id` (string): Return results that are actions performed by the user indicated by this User ID
* `query_file_id` (string): Return results that are file actions related to the file indicated by this File ID
* `query_parent_id` (string): Return results that are file actions inside the parent folder specified by this folder ID
* `query_path` (string): Return results that are file actions related to paths matching this pattern.
* `query_folder` (string): Return results that are file actions related to files or folders inside folder paths matching this pattern.
* `query_src` (string): Return results that are file moves originating from paths matching this pattern.
* `query_destination` (string): Return results that are file moves with paths matching this pattern as destination.
* `query_ip` (string): Filter results by this IP address.
* `query_username` (string): Filter results by this username.
* `query_failure_type` (string): If searching for Histories about login failures, this parameter restricts results to failures of this specific type.  Valid values: `expired_trial`, `account_overdue`, `locked_out`, `ip_mismatch`, `password_mismatch`, `site_mismatch`, `username_not_found`, `none`, `no_ftp_permission`, `no_web_permission`, `no_directory`, `errno_enoent`, `no_sftp_permission`, `no_dav_permission`, `no_restapi_permission`, `key_mismatch`, `region_mismatch`, `expired_access`, `desktop_ip_mismatch`, `desktop_api_key_not_used_quickly_enough`, `disabled`, `country_mismatch`, `insecure_ftp`, `insecure_cipher`, `rate_limited`
* `query_target_id` (string): If searching for Histories about specific objects (such as Users, or API Keys), this parameter restricts results to objects that match this ID.
* `query_target_name` (string): If searching for Histories about Users, Groups or other objects with names, this parameter restricts results to objects with this name/username.
* `query_target_permission` (string): If searching for Histories about Permissions, this parameter restricts results to permissions of this level.
* `query_target_user_id` (string): If searching for Histories about API keys, this parameter restricts results to API keys created by/for this user ID.
* `query_target_username` (string): If searching for Histories about API keys, this parameter restricts results to API keys created by/for this username.
* `query_target_platform` (string): If searching for Histories about API keys, this parameter restricts results to API keys associated with this platform.
* `query_target_permission_set` (string): If searching for Histories about API keys, this parameter restricts results to API keys with this permission set.
* `results_url` (string): If `status` is `ready`, this will be a URL where all the results can be downloaded at once as a CSV.
* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.


---

## Show History Export

```
files_sdk.history_export.find(id)
```

### Parameters

* `id` (int64): Required - History Export ID.


---

## Create History Export

```
files_sdk.history_export.create({
  "user_id": 1,
  "start_at": "2000-01-01T01:00:00Z",
  "end_at": "2000-01-01T01:00:00Z",
  "query_action": "read",
  "query_interface": "ftp",
  "query_user_id": "1",
  "query_file_id": "1",
  "query_parent_id": "1",
  "query_path": "MyFile.txt",
  "query_folder": "Folder",
  "query_src": "SrcFolder",
  "query_destination": "DestFolder",
  "query_ip": "127.0.0.1",
  "query_username": "jerry",
  "query_failure_type": "bad_password",
  "query_target_id": "1",
  "query_target_name": "full",
  "query_target_permission": "full",
  "query_target_user_id": "1",
  "query_target_username": "jerry",
  "query_target_platform": "windows",
  "query_target_permission_set": "desktop_app"
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `start_at` (string): Start date/time of export range.
* `end_at` (string): End date/time of export range.
* `query_action` (string): Filter results by this this action type. Valid values: `create`, `read`, `update`, `destroy`, `move`, `login`, `failedlogin`, `copy`, `user_create`, `user_update`, `user_destroy`, `group_create`, `group_update`, `group_destroy`, `permission_create`, `permission_destroy`, `api_key_create`, `api_key_update`, `api_key_destroy`
* `query_interface` (string): Filter results by this this interface type. Valid values: `web`, `ftp`, `robot`, `jsapi`, `webdesktopapi`, `sftp`, `dav`, `desktop`, `restapi`, `scim`, `office`, `mobile`, `as2`, `inbound_email`, `remote`
* `query_user_id` (string): Return results that are actions performed by the user indicated by this User ID
* `query_file_id` (string): Return results that are file actions related to the file indicated by this File ID
* `query_parent_id` (string): Return results that are file actions inside the parent folder specified by this folder ID
* `query_path` (string): Return results that are file actions related to paths matching this pattern.
* `query_folder` (string): Return results that are file actions related to files or folders inside folder paths matching this pattern.
* `query_src` (string): Return results that are file moves originating from paths matching this pattern.
* `query_destination` (string): Return results that are file moves with paths matching this pattern as destination.
* `query_ip` (string): Filter results by this IP address.
* `query_username` (string): Filter results by this username.
* `query_failure_type` (string): If searching for Histories about login failures, this parameter restricts results to failures of this specific type.  Valid values: `expired_trial`, `account_overdue`, `locked_out`, `ip_mismatch`, `password_mismatch`, `site_mismatch`, `username_not_found`, `none`, `no_ftp_permission`, `no_web_permission`, `no_directory`, `errno_enoent`, `no_sftp_permission`, `no_dav_permission`, `no_restapi_permission`, `key_mismatch`, `region_mismatch`, `expired_access`, `desktop_ip_mismatch`, `desktop_api_key_not_used_quickly_enough`, `disabled`, `country_mismatch`, `insecure_ftp`, `insecure_cipher`, `rate_limited`
* `query_target_id` (string): If searching for Histories about specific objects (such as Users, or API Keys), this parameter restricts results to objects that match this ID.
* `query_target_name` (string): If searching for Histories about Users, Groups or other objects with names, this parameter restricts results to objects with this name/username.
* `query_target_permission` (string): If searching for Histories about Permissions, this parameter restricts results to permissions of this level.
* `query_target_user_id` (string): If searching for Histories about API keys, this parameter restricts results to API keys created by/for this user ID.
* `query_target_username` (string): If searching for Histories about API keys, this parameter restricts results to API keys created by/for this username.
* `query_target_platform` (string): If searching for Histories about API keys, this parameter restricts results to API keys associated with this platform.
* `query_target_permission_set` (string): If searching for Histories about API keys, this parameter restricts results to API keys with this permission set.

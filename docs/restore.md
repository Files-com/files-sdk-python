# Restore

## Example Restore Object

```
{
  "earliest_date": "2000-01-01T01:00:00Z",
  "id": 1,
  "dirs_restored": 1,
  "dirs_errored": 1,
  "dirs_total": 1,
  "files_restored": 1,
  "files_errored": 1,
  "files_total": 1,
  "prefix": "foo/bar/baz.txt",
  "restore_in_place": True,
  "restore_deleted_permissions": True,
  "status": "pending",
  "update_timestamps": True,
  "error_messages": [
    "example"
  ]
}
```

* `earliest_date` (date-time): Restore all files deleted after this date/time. Don't set this earlier than you need. Can not be greater than 365 days prior to the restore request.
* `id` (int64): Restore Record ID.
* `dirs_restored` (int64): Number of directories that were successfully restored.
* `dirs_errored` (int64): Number of directories that were not able to be restored.
* `dirs_total` (int64): Total number of directories processed.
* `files_restored` (int64): Number of files successfully restored.
* `files_errored` (int64): Number of files that were not able to be restored.
* `files_total` (int64): Total number of files processed.
* `prefix` (string): Prefix of the files/folders to restore. To restore a folder, add a trailing slash to the folder name. Do not use a leading slash. To restore all deleted items, specify an empty string (`''`) in the prefix field or omit the field from the request.
* `restore_in_place` (boolean): If true, we will restore the files in place (into their original paths). If false, we will create a new restoration folder in the root and restore files there.
* `restore_deleted_permissions` (boolean): If true, we will also restore any Permissions that match the same path prefix from the same dates.
* `status` (string): Status of the restoration process.
* `update_timestamps` (boolean): If true, we will update the last modified timestamp of restored files to today's date. If false, we might trigger File Expiration to delete the file again.
* `error_messages` (array(string)): Error messages received while restoring files and/or directories. Only present if there were errors.


---

## List Restores

```
files_sdk.restore.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Create Restore

```
files_sdk.restore.create({
  "earliest_date": "2000-01-01T01:00:00Z",
  "prefix": "foo/bar/baz.txt",
  "restore_deleted_permissions": True,
  "restore_in_place": True,
  "update_timestamps": True
})
```

### Parameters

* `earliest_date` (string): Required - Restore all files deleted after this date/time. Don't set this earlier than you need. Can not be greater than 365 days prior to the restore request.
* `prefix` (string): Prefix of the files/folders to restore. To restore a folder, add a trailing slash to the folder name. Do not use a leading slash. To restore all deleted items, specify an empty string (`''`) in the prefix field or omit the field from the request.
* `restore_deleted_permissions` (boolean): If true, we will also restore any Permissions that match the same path prefix from the same dates.
* `restore_in_place` (boolean): If true, we will restore the files in place (into their original paths). If false, we will create a new restoration folder in the root and restore files there.
* `update_timestamps` (boolean): If true, we will update the last modified timestamp of restored files to today's date. If false, we might trigger File Expiration to delete the file again.

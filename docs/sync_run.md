# SyncRun

## Example SyncRun Object

```
{
  "id": 1,
  "body": "example",
  "bytes_synced": 1,
  "compared_files": 1,
  "compared_folders": 1,
  "completed_at": "2000-01-01T01:00:00Z",
  "created_at": "2000-01-01T01:00:00Z",
  "dest_remote_server_type": "example",
  "dry_run": True,
  "errored_files": 1,
  "estimated_bytes_count": 1,
  "event_errors": [
    "example"
  ],
  "log_url": "https://www.example.com/log_file.txt",
  "runtime": 1.0,
  "site_id": 1,
  "workspace_id": 1,
  "src_remote_server_type": "example",
  "status": "example",
  "successful_files": 1,
  "sync_id": 1,
  "sync_name": "Azure to SharePoint Sync",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): SyncRun ID
* `body` (string): Log or summary body for this run
* `bytes_synced` (int64): Total bytes synced in this run
* `compared_files` (int64): Number of files compared
* `compared_folders` (int64): Number of folders compared
* `completed_at` (date-time): When this run was completed
* `created_at` (date-time): When this run was created
* `dest_remote_server_type` (string): Destination remote server type, if any
* `dry_run` (boolean): Whether this run was a dry run (no actual changes made)
* `errored_files` (int64): Number of files that errored
* `estimated_bytes_count` (int64): Estimated bytes count for this run
* `event_errors` (array(string)): Array of errors encountered during the run
* `log_url` (string): Link to external log file.
* `runtime` (double): Total runtime in seconds
* `site_id` (int64): Site ID
* `workspace_id` (int64): Workspace ID
* `src_remote_server_type` (string): Source remote server type, if any
* `status` (string): Status of the sync run (success, failure, partial_failure, in_progress, skipped)
* `successful_files` (int64): Number of files successfully synced
* `sync_id` (int64): ID of the Sync this run belongs to
* `sync_name` (string): Name of the Sync this run belongs to
* `updated_at` (date-time): When this run was last updated


---

## List Sync Runs

```
files_sdk.sync_run.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `workspace_id`, `sync_id`, `created_at` or `status`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `status`, `dry_run`, `workspace_id`, `src_remote_server_type`, `dest_remote_server_type` or `sync_id`. Valid field combinations are `[ status, created_at ]`, `[ workspace_id, created_at ]`, `[ src_remote_server_type, created_at ]`, `[ dest_remote_server_type, created_at ]`, `[ sync_id, created_at ]`, `[ workspace_id, status ]`, `[ src_remote_server_type, status ]`, `[ dest_remote_server_type, status ]`, `[ sync_id, status ]`, `[ workspace_id, src_remote_server_type ]`, `[ workspace_id, dest_remote_server_type ]`, `[ workspace_id, sync_id ]`, `[ workspace_id, status, created_at ]`, `[ src_remote_server_type, status, created_at ]`, `[ dest_remote_server_type, status, created_at ]`, `[ sync_id, status, created_at ]`, `[ workspace_id, src_remote_server_type, created_at ]`, `[ workspace_id, dest_remote_server_type, created_at ]`, `[ workspace_id, sync_id, created_at ]`, `[ workspace_id, src_remote_server_type, status ]`, `[ workspace_id, dest_remote_server_type, status ]`, `[ workspace_id, sync_id, status ]`, `[ workspace_id, src_remote_server_type, status, created_at ]`, `[ workspace_id, dest_remote_server_type, status, created_at ]` or `[ workspace_id, sync_id, status, created_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.


---

## Show Sync Run

```
files_sdk.sync_run.find(id)
```

### Parameters

* `id` (int64): Required - Sync Run ID.

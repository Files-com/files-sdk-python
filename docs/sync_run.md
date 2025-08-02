# SyncRun

## Example SyncRun Object

```
{
  "id": 1,
  "sync_id": 1,
  "site_id": 1,
  "status": "example",
  "src_remote_server_type": "example",
  "dest_remote_server_type": "example",
  "body": "example",
  "event_errors": [
    "example"
  ],
  "compared_files": 1,
  "compared_folders": 1,
  "errored_files": 1,
  "successful_files": 1,
  "runtime": 1.0,
  "log_url": "https://www.example.com/log_file.txt",
  "completed_at": "2000-01-01T01:00:00Z",
  "notified": True,
  "dry_run": True,
  "bytes_synced": 1,
  "estimated_bytes_count": 1,
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): SyncRun ID
* `sync_id` (int64): ID of the Sync this run belongs to
* `site_id` (int64): Site ID
* `status` (string): Status of the sync run (success, failure, partial_failure, in_progress, skipped)
* `src_remote_server_type` (string): Source remote server type, if any
* `dest_remote_server_type` (string): Destination remote server type, if any
* `body` (string): Log or summary body for this run
* `event_errors` (array(string)): Array of errors encountered during the run
* `compared_files` (int64): Number of files compared
* `compared_folders` (int64): Number of folders compared
* `errored_files` (int64): Number of files that errored
* `successful_files` (int64): Number of files successfully synced
* `runtime` (double): Total runtime in seconds
* `log_url` (string): Link to external log file.
* `completed_at` (date-time): When this run was completed
* `notified` (boolean): Whether notifications were sent for this run
* `dry_run` (boolean): Whether this run was a dry run (no actual changes made)
* `bytes_synced` (int64): Total bytes synced in this run
* `estimated_bytes_count` (int64): Estimated bytes count for this run
* `created_at` (date-time): When this run was created
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
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `site_id`, `sync_id` or `created_at`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `status`, `dry_run` or `sync_id`. Valid field combinations are `[ sync_id, status ]`.


---

## Show Sync Run

```
files_sdk.sync_run.find(id)
```

### Parameters

* `id` (int64): Required - Sync Run ID.

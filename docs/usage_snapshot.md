# UsageSnapshot

## Example UsageSnapshot Object

```
{
  "id": 1,
  "start_at": "2000-01-01T01:00:00Z",
  "end_at": "2000-01-01T01:00:00Z",
  "high_water_user_count": 1,
  "current_storage": 1.0,
  "high_water_storage": 1.0,
  "root_storage": 1.0,
  "deleted_files_counted_in_minimum": 1.0,
  "deleted_files_storage": 1.0,
  "total_billable_usage": 1.0,
  "total_billable_transfer_usage": 1.0,
  "bytes_sent": 1.0,
  "sync_bytes_received": 1.0,
  "sync_bytes_sent": 1.0,
  "usage_by_top_level_dir": [
    {
      "dir": "dir",
      "size": 100,
      "count": 10
    }
  ]
}
```

* `id` (int64): Usage snapshot ID
* `start_at` (date-time): Usage snapshot start date/time
* `end_at` (date-time): Usage snapshot end date/time
* `high_water_user_count` (int64): Highest user count number in time period
* `current_storage` (double): Current total Storage Usage GB as of end date (not necessarily high water mark, which is used for billing)
* `high_water_storage` (double): Highest Storage Usage GB recorded in time period (used for billing)
* `root_storage` (double): Storage Usage for root folder as of end date (not necessarily high water mark, which is used for billing)
* `deleted_files_counted_in_minimum` (double): Storage Usage for files that are deleted but uploaded within last 30 days as of end date (not necessarily high water mark, which is used for billing)
* `deleted_files_storage` (double): Storage Usage for files that are deleted but retained as backups as of end date (not necessarily high water mark, which is used for billing)
* `total_billable_usage` (double): Storage + Transfer Usage - Total Billable amount
* `total_billable_transfer_usage` (double): Transfer usage for period - Total Billable amount
* `bytes_sent` (double): Transfer Usage for period - Outbound GB from Files Native Storage
* `sync_bytes_received` (double): Transfer Usage for period - Inbound GB to Remote Servers (Sync/Mount)
* `sync_bytes_sent` (double): Transfer Usage for period - Outbound GB from Remote Servers (Sync/Mount)
* `usage_by_top_level_dir` (array(object)): Storage Usage - map of root folders to their usage as of end date (not necessarily high water mark, which is used for billing)


---

## List Usage Snapshots

```
files_sdk.usage_snapshot.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).

# UsageSnapshot

## Example UsageSnapshot Object

```
{
  "id": 1,
  "start_at": "2000-01-01T01:00:00Z",
  "end_at": "2000-01-01T01:00:00Z",
  "created_at": "2000-01-01T01:00:00Z",
  "high_water_user_count": 1.0,
  "current_storage": 1.0,
  "high_water_storage": 1.0,
  "total_downloads": 1,
  "total_uploads": 1,
  "updated_at": "2000-01-01T01:00:00Z",
  "usage_by_top_level_dir": "",
  "root_storage": 1.0,
  "deleted_files_counted_in_minimum": 1.0,
  "deleted_files_storage": 1.0
}
```

* `id` (int64): Site usage ID
* `start_at` (date-time): Site usage report start date/time
* `end_at` (date-time): Site usage report end date/time
* `created_at` (date-time): Site usage report created at date/time
* `high_water_user_count` (double): Site usage report highest usage in time period
* `current_storage` (double): Current site usage as of report
* `high_water_storage` (double): Site usage report highest usage in time period
* `total_downloads` (int64): Number of downloads in report time period
* `total_uploads` (int64): Number of uploads in time period
* `updated_at` (date-time): The last time this site usage report was updated
* `usage_by_top_level_dir` (object): A map of root folders to their total usage
* `root_storage` (double): Usage for root folder
* `deleted_files_counted_in_minimum` (double): Usage for files that are deleted but uploaded within last 30 days
* `deleted_files_storage` (double): Usage for files that are deleted but retained as backups


---

## List Usage Snapshots

```
files_sdk.usage_snapshot.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).

# UsageDailySnapshot

## Example UsageDailySnapshot Object

```
{
  "id": 1,
  "date": "2000-01-01T01:00:00Z",
  "api_usage_available": True,
  "read_api_usage": 1,
  "write_api_usage": 1,
  "user_count": 1,
  "current_storage": 1,
  "deleted_files_storage": 1,
  "deleted_files_counted_in_minimum": 1,
  "root_storage": 1,
  "usage_by_top_level_dir": {
    "key": "example value"
  }
}
```

* `id` (int64): ID of the usage record
* `date` (date): The date of this usage record
* `api_usage_available` (boolean): True if the API usage fields `read_api_usage` and `write_api_usage` can be relied upon.  If this is false, we suggest hiding that value from any UI.
* `read_api_usage` (int64): Read API Calls used on this day. Note: only updated for days before the current day.
* `write_api_usage` (int64): Write API Calls used on this day. Note: only updated for days before the current day.
* `user_count` (int64): Number of billable users as of this day.
* `current_storage` (int64): GB of Files Native Storage used on this day.
* `deleted_files_storage` (int64): GB of Files Native Storage used on this day for files that have been deleted and are stored as backups.
* `deleted_files_counted_in_minimum` (int64): GB of Files Native Storage used on this day for files that have been permanently deleted but were uploaded less than 30 days ago, and are still billable.
* `root_storage` (int64): GB of Files Native Storage used for the root folder.  Included here because this value will not be part of `usage_by_top_level_dir`
* `usage_by_top_level_dir` (object): Usage broken down by each top-level folder


---

## List Usage Daily Snapshots

```
files_sdk.usage_daily_snapshot.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `date` and `usage_snapshot_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.
* `filter_like` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `date` and `usage_snapshot_id`. Valid field combinations are `[ usage_snapshot_id, date ]`.

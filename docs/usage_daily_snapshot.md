# UsageDailySnapshot

## Example UsageDailySnapshot Object

```
{
  "id": 1,
  "date": "2020-11-21",
  "current_storage": "65536",
  "usage_by_top_level_dir": [

  ]
}
```

* `id` (int64): ID of the usage record
* `date` (date): The date of this usage record
* `current_storage` (int64): The quantity of storage held for this site
* `usage_by_top_level_dir` (array): Usage broken down by each top-level folder


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

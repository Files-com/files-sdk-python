# Sync

## Example Sync Object

```
{
  "id": 1,
  "name": "example",
  "description": "example",
  "site_id": 1,
  "user_id": 1,
  "src_path": "example",
  "dest_path": "example",
  "src_remote_server_id": 1,
  "dest_remote_server_id": 1,
  "two_way": True,
  "keep_after_copy": True,
  "delete_empty_folders": True,
  "disabled": True,
  "trigger": "example",
  "trigger_file": "example",
  "include_patterns": [
    "example"
  ],
  "exclude_patterns": [
    "example"
  ],
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z",
  "sync_interval_minutes": 1,
  "interval": "week",
  "recurring_day": 25,
  "schedule_days_of_week": [
    0,
    2,
    4
  ],
  "schedule_times_of_day": [
    "06:30",
    "14:30"
  ],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us_dc",
  "latest_sync_run": {
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
}
```

* `id` (int64): Sync ID
* `name` (string): Name for this sync job
* `description` (string): Description for this sync job
* `site_id` (int64): Site ID this sync belongs to
* `user_id` (int64): User who created or owns this sync
* `src_path` (string): Absolute source path for the sync
* `dest_path` (string): Absolute destination path for the sync
* `src_remote_server_id` (int64): Remote server ID for the source (if remote)
* `dest_remote_server_id` (int64): Remote server ID for the destination (if remote)
* `two_way` (boolean): Is this a two-way sync?
* `keep_after_copy` (boolean): Keep files after copying?
* `delete_empty_folders` (boolean): Delete empty folders after sync?
* `disabled` (boolean): Is this sync disabled?
* `trigger` (string): Trigger type: daily, custom_schedule, or manual
* `trigger_file` (string): Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
* `include_patterns` (array(string)): Array of glob patterns to include
* `exclude_patterns` (array(string)): Array of glob patterns to exclude
* `created_at` (date-time): When this sync was created
* `updated_at` (date-time): When this sync was last updated
* `sync_interval_minutes` (int64): Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
* `interval` (string): If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
* `schedule_times_of_day` (array(string)): If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. Times of day in HH:MM format.
* `schedule_time_zone` (string): If trigger is `custom_schedule`, Custom schedule Time Zone for when the sync should be run.
* `holiday_region` (string): If trigger is `custom_schedule`, the sync will check if there is a formal, observed holiday for the region, and if so, it will not run.
* `latest_sync_run` (SyncRun): The latest run of this sync


---

## List Syncs

```
files_sdk.sync.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Show Sync

```
files_sdk.sync.find(id)
```

### Parameters

* `id` (int64): Required - Sync ID.


---

## Create Sync

```
files_sdk.sync.create({
  "name": "example",
  "description": "example",
  "src_path": "example",
  "dest_path": "example",
  "src_remote_server_id": 1,
  "dest_remote_server_id": 1,
  "two_way": False,
  "keep_after_copy": False,
  "delete_empty_folders": False,
  "disabled": False,
  "interval": "week",
  "trigger": "example",
  "trigger_file": "example",
  "holiday_region": "us_dc",
  "sync_interval_minutes": 1,
  "recurring_day": 25,
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "schedule_days_of_week": [0,2,4],
  "schedule_times_of_day": ["06:30","14:30"]
})
```

### Parameters

* `name` (string): Name for this sync job
* `description` (string): Description for this sync job
* `src_path` (string): Absolute source path
* `dest_path` (string): Absolute destination path
* `src_remote_server_id` (int64): Remote server ID for the source
* `dest_remote_server_id` (int64): Remote server ID for the destination
* `two_way` (boolean): Is this a two-way sync?
* `keep_after_copy` (boolean): Keep files after copying?
* `delete_empty_folders` (boolean): Delete empty folders after sync?
* `disabled` (boolean): Is this sync disabled?
* `interval` (string): If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `trigger` (string): Trigger type: daily, custom_schedule, or manual
* `trigger_file` (string): Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
* `holiday_region` (string): If trigger is `custom_schedule`, the sync will check if there is a formal, observed holiday for the region, and if so, it will not run.
* `sync_interval_minutes` (int64): Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `schedule_time_zone` (string): If trigger is `custom_schedule`, Custom schedule Time Zone for when the sync should be run.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
* `schedule_times_of_day` (array(string)): If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. Times of day in HH:MM format.


---

## Dry Run Sync

```
files_sdk.sync.dry_run(id)
```

### Parameters

* `id` (int64): Required - Sync ID.


---

## Manually Run Sync

```
files_sdk.sync.manual_run(id)
```

### Parameters

* `id` (int64): Required - Sync ID.


---

## Update Sync

```
files_sdk.sync.update(id, {
  "name": "example",
  "description": "example",
  "src_path": "example",
  "dest_path": "example",
  "src_remote_server_id": 1,
  "dest_remote_server_id": 1,
  "two_way": False,
  "keep_after_copy": False,
  "delete_empty_folders": False,
  "disabled": False,
  "interval": "week",
  "trigger": "example",
  "trigger_file": "example",
  "holiday_region": "us_dc",
  "sync_interval_minutes": 1,
  "recurring_day": 25,
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "schedule_days_of_week": [0,2,4],
  "schedule_times_of_day": ["06:30","14:30"]
})
```

### Parameters

* `id` (int64): Required - Sync ID.
* `name` (string): Name for this sync job
* `description` (string): Description for this sync job
* `src_path` (string): Absolute source path
* `dest_path` (string): Absolute destination path
* `src_remote_server_id` (int64): Remote server ID for the source
* `dest_remote_server_id` (int64): Remote server ID for the destination
* `two_way` (boolean): Is this a two-way sync?
* `keep_after_copy` (boolean): Keep files after copying?
* `delete_empty_folders` (boolean): Delete empty folders after sync?
* `disabled` (boolean): Is this sync disabled?
* `interval` (string): If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `trigger` (string): Trigger type: daily, custom_schedule, or manual
* `trigger_file` (string): Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
* `holiday_region` (string): If trigger is `custom_schedule`, the sync will check if there is a formal, observed holiday for the region, and if so, it will not run.
* `sync_interval_minutes` (int64): Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `schedule_time_zone` (string): If trigger is `custom_schedule`, Custom schedule Time Zone for when the sync should be run.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
* `schedule_times_of_day` (array(string)): If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. Times of day in HH:MM format.


---

## Delete Sync

```
files_sdk.sync.delete(id)
```

### Parameters

* `id` (int64): Required - Sync ID.


---

## Dry Run Sync

```
sync = files_sdk.sync.find(id)
sync.dry_run()
```

### Parameters

* `id` (int64): Required - Sync ID.


---

## Manually Run Sync

```
sync = files_sdk.sync.find(id)
sync.manual_run()
```

### Parameters

* `id` (int64): Required - Sync ID.


---

## Update Sync

```
sync = files_sdk.sync.find(id)
sync.update({
  "name": "example",
  "description": "example",
  "src_path": "example",
  "dest_path": "example",
  "src_remote_server_id": 1,
  "dest_remote_server_id": 1,
  "two_way": False,
  "keep_after_copy": False,
  "delete_empty_folders": False,
  "disabled": False,
  "interval": "week",
  "trigger": "example",
  "trigger_file": "example",
  "holiday_region": "us_dc",
  "sync_interval_minutes": 1,
  "recurring_day": 25,
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "schedule_days_of_week": [0,2,4],
  "schedule_times_of_day": ["06:30","14:30"]
})
```

### Parameters

* `id` (int64): Required - Sync ID.
* `name` (string): Name for this sync job
* `description` (string): Description for this sync job
* `src_path` (string): Absolute source path
* `dest_path` (string): Absolute destination path
* `src_remote_server_id` (int64): Remote server ID for the source
* `dest_remote_server_id` (int64): Remote server ID for the destination
* `two_way` (boolean): Is this a two-way sync?
* `keep_after_copy` (boolean): Keep files after copying?
* `delete_empty_folders` (boolean): Delete empty folders after sync?
* `disabled` (boolean): Is this sync disabled?
* `interval` (string): If trigger is `daily`, this specifies how often to run this sync.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `trigger` (string): Trigger type: daily, custom_schedule, or manual
* `trigger_file` (string): Some MFT services request an empty file (known as a trigger file) to signal the sync is complete and they can begin further processing. If trigger_file is set, a zero-byte file will be sent at the end of the sync.
* `holiday_region` (string): If trigger is `custom_schedule`, the sync will check if there is a formal, observed holiday for the region, and if so, it will not run.
* `sync_interval_minutes` (int64): Frequency in minutes between syncs. If set, this value must be greater than or equal to the `remote_sync_interval` value for the site's plan. If left blank, the plan's `remote_sync_interval` will be used. This setting is only used if `trigger` is empty.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `schedule_time_zone` (string): If trigger is `custom_schedule`, Custom schedule Time Zone for when the sync should be run.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
* `schedule_times_of_day` (array(string)): If trigger is `custom_schedule`, Custom schedule description for when the sync should be run. Times of day in HH:MM format.


---

## Delete Sync

```
sync = files_sdk.sync.find(id)
sync.delete()
```

### Parameters

* `id` (int64): Required - Sync ID.

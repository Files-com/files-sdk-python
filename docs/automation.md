# Automation

## Example Automation Object

```
{
  "id": 1,
  "always_serialize_jobs": True,
  "always_overwrite_size_matching_files": True,
  "automation": "create_folder",
  "deleted": True,
  "description": "example",
  "destination_replace_from": "example",
  "destination_replace_to": "example",
  "destinations": [
    "destination"
  ],
  "disabled": True,
  "exclude_pattern": "path/to/exclude/*",
  "import_urls": [
    {
      "name": "users.json",
      "url": "http://example.com/users",
      "method": "POST",
      "headers": {
        "Content-Type": "application/json"
      },
      "content": {
        "group": "support"
      }
    }
  ],
  "flatten_destination_structure": True,
  "group_ids": [
    1,
    2
  ],
  "ignore_locked_folders": True,
  "interval": "week",
  "last_modified_at": "2000-01-01T01:00:00Z",
  "legacy_folder_matching": True,
  "name": "example",
  "overwrite_files": True,
  "path": "example",
  "path_time_zone": "Eastern Time (US & Canada)",
  "recurring_day": 25,
  "retry_on_failure_interval_in_minutes": 60,
  "retry_on_failure_number_of_attempts": 10,
  "schedule": {
    "days_of_week": [
      0,
      2,
      4
    ],
    "times_of_day": [
      "06:30",
      "14:30"
    ],
    "time_zone": "Eastern Time (US & Canada)"
  },
  "human_readable_schedule": "Triggered every Monday, Wednesday at 6:30 AM,\n  2:30 PM Eastern Time (US & Canada) TZ",
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
  "source": "example",
  "sync_ids": [
    1,
    2
  ],
  "trigger_actions": [
    "create"
  ],
  "trigger": "daily",
  "user_id": 1,
  "user_ids": [
    1,
    2
  ],
  "value": {
    "limit": "1"
  },
  "webhook_url": "https://app.files.com/api/webhooks/abc123"
}
```

* `id` (int64): Automation ID
* `always_serialize_jobs` (boolean): Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
* `always_overwrite_size_matching_files` (boolean): Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
* `automation` (string): Automation type
* `deleted` (boolean): Indicates if the automation has been deleted.
* `description` (string): Description for the this Automation.
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `destinations` (array(string)): Destination Paths
* `disabled` (boolean): If true, this automation will not run.
* `exclude_pattern` (string): If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
* `import_urls` (array(object)): List of URLs to be imported and names to be used.
* `flatten_destination_structure` (boolean): Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
* `group_ids` (array(int64)): IDs of Groups for the Automation (i.e. who to Request File from)
* `ignore_locked_folders` (boolean): If true, the Lock Folders behavior will be disregarded for automated actions.
* `interval` (string): If trigger is `daily`, this specifies how often to run this automation.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `last_modified_at` (date-time): Time when automation was last modified. Does not change for name or description updates.
* `legacy_folder_matching` (boolean): If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
* `name` (string): Name for this automation.
* `overwrite_files` (boolean): If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
* `path` (string): Path on which this Automation runs.  Supports globs, except on remote mounts. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `path_time_zone` (string): Timezone to use when rendering timestamps in paths.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `retry_on_failure_interval_in_minutes` (int64): If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
* `retry_on_failure_number_of_attempts` (int64): If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
* `schedule` (object): If trigger is `custom_schedule`, Custom schedule description for when the automation should be run in json format.
* `human_readable_schedule` (string): If trigger is `custom_schedule`, Human readable Custom schedule description for when the automation should be run.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, Custom schedule description for when the automation should be run. 0-based days of the week. 0 is Sunday, 1 is Monday, etc.
* `schedule_times_of_day` (array(string)): If trigger is `custom_schedule`, Custom schedule description for when the automation should be run. Times of day in HH:MM format.
* `schedule_time_zone` (string): If trigger is `custom_schedule`, Custom schedule Time Zone for when the automation should be run.
* `source` (string): Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
* `sync_ids` (array(int64)): IDs of remote sync folder behaviors to run by this Automation
* `trigger_actions` (array(string)): If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
* `trigger` (string): How this automation is triggered to run.
* `user_id` (int64): User ID of the Automation's creator.
* `user_ids` (array(int64)): IDs of Users for the Automation (i.e. who to Request File from)
* `value` (object): A Hash of attributes specific to the automation type.
* `webhook_url` (string): If trigger is `webhook`, this is the URL of the webhook to trigger the Automation.


---

## List Automations

```
files_sdk.automation.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `automation`, `disabled`, `last_modified_at` or `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `last_modified_at` or `automation`. Valid field combinations are `[ disabled, last_modified_at ]`, `[ automation, disabled ]`, `[ automation, last_modified_at ]` or `[ automation, disabled, last_modified_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `last_modified_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `last_modified_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `last_modified_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `last_modified_at`.


---

## Show Automation

```
files_sdk.automation.find(id)
```

### Parameters

* `id` (int64): Required - Automation ID.


---

## Create Automation

```
files_sdk.automation.create({
  "source": "example",
  "destinations": ["folder_a/file_a.txt",{"folder_path":"folder_b","file_path":"file_b.txt"},{"folder_path":"folder_c"}],
  "destination_replace_from": "example",
  "destination_replace_to": "example",
  "interval": "year",
  "path": "example",
  "sync_ids": [1,2],
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule_days_of_week": [0,1,3],
  "schedule_times_of_day": ["7:30","11:30"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "always_overwrite_size_matching_files": True,
  "always_serialize_jobs": True,
  "description": "example",
  "disabled": True,
  "exclude_pattern": "path/to/exclude/*",
  "import_urls": [{"name":"users.json","url":"http://example.com/users","method":"POST","headers":{"Content-Type":"application/json"},"content":{"group":"support"}}],
  "flatten_destination_structure": True,
  "ignore_locked_folders": True,
  "legacy_folder_matching": False,
  "name": "example",
  "overwrite_files": True,
  "path_time_zone": "Eastern Time (US & Canada)",
  "retry_on_failure_interval_in_minutes": 60,
  "retry_on_failure_number_of_attempts": 10,
  "trigger": "daily",
  "trigger_actions": ["create"],
  "value": {"limit":"1"},
  "recurring_day": 25,
  "automation": "create_folder"
})
```

### Parameters

* `source` (string): Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
* `destinations` (array(string)): A list of String destination paths or Hash of folder_path and optional file_path.
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs, except on remote mounts.
* `sync_ids` (string): A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`. A list of days of the week to run this automation. 0 is Sunday, 1 is Monday, etc.
* `schedule_times_of_day` (array(string)): If trigger is `custom_schedule`. A list of times of day to run this automation. 24-hour time format.
* `schedule_time_zone` (string): If trigger is `custom_schedule`. Time zone for the schedule.
* `always_overwrite_size_matching_files` (boolean): Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
* `always_serialize_jobs` (boolean): Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
* `description` (string): Description for the this Automation.
* `disabled` (boolean): If true, this automation will not run.
* `exclude_pattern` (string): If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
* `import_urls` (array(object)): List of URLs to be imported and names to be used.
* `flatten_destination_structure` (boolean): Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
* `ignore_locked_folders` (boolean): If true, the Lock Folders behavior will be disregarded for automated actions.
* `legacy_folder_matching` (boolean): DEPRECATED: If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
* `name` (string): Name for this automation.
* `overwrite_files` (boolean): If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
* `path_time_zone` (string): Timezone to use when rendering timestamps in paths.
* `retry_on_failure_interval_in_minutes` (int64): If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
* `retry_on_failure_number_of_attempts` (int64): If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
* `trigger` (string): How this automation is triggered to run.
* `trigger_actions` (array(string)): If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
* `value` (object): A Hash of attributes specific to the automation type.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `automation` (string): Required - Automation type


---

## Manually Run Automation

```
files_sdk.automation.manual_run(id)
```

### Parameters

* `id` (int64): Required - Automation ID.


---

## Update Automation

```
files_sdk.automation.update(id, {
  "source": "example",
  "destinations": ["folder_a/file_a.txt",{"folder_path":"folder_b","file_path":"file_b.txt"},{"folder_path":"folder_c"}],
  "destination_replace_from": "example",
  "destination_replace_to": "example",
  "interval": "year",
  "path": "example",
  "sync_ids": [1,2],
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule_days_of_week": [0,1,3],
  "schedule_times_of_day": ["7:30","11:30"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "always_overwrite_size_matching_files": True,
  "always_serialize_jobs": True,
  "description": "example",
  "disabled": True,
  "exclude_pattern": "path/to/exclude/*",
  "import_urls": [{"name":"users.json","url":"http://example.com/users","method":"POST","headers":{"Content-Type":"application/json"},"content":{"group":"support"}}],
  "flatten_destination_structure": True,
  "ignore_locked_folders": True,
  "legacy_folder_matching": False,
  "name": "example",
  "overwrite_files": True,
  "path_time_zone": "Eastern Time (US & Canada)",
  "retry_on_failure_interval_in_minutes": 60,
  "retry_on_failure_number_of_attempts": 10,
  "trigger": "daily",
  "trigger_actions": ["create"],
  "value": {"limit":"1"},
  "recurring_day": 25,
  "automation": "create_folder"
})
```

### Parameters

* `id` (int64): Required - Automation ID.
* `source` (string): Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
* `destinations` (array(string)): A list of String destination paths or Hash of folder_path and optional file_path.
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs, except on remote mounts.
* `sync_ids` (string): A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`. A list of days of the week to run this automation. 0 is Sunday, 1 is Monday, etc.
* `schedule_times_of_day` (array(string)): If trigger is `custom_schedule`. A list of times of day to run this automation. 24-hour time format.
* `schedule_time_zone` (string): If trigger is `custom_schedule`. Time zone for the schedule.
* `always_overwrite_size_matching_files` (boolean): Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
* `always_serialize_jobs` (boolean): Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
* `description` (string): Description for the this Automation.
* `disabled` (boolean): If true, this automation will not run.
* `exclude_pattern` (string): If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
* `import_urls` (array(object)): List of URLs to be imported and names to be used.
* `flatten_destination_structure` (boolean): Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
* `ignore_locked_folders` (boolean): If true, the Lock Folders behavior will be disregarded for automated actions.
* `legacy_folder_matching` (boolean): DEPRECATED: If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
* `name` (string): Name for this automation.
* `overwrite_files` (boolean): If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
* `path_time_zone` (string): Timezone to use when rendering timestamps in paths.
* `retry_on_failure_interval_in_minutes` (int64): If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
* `retry_on_failure_number_of_attempts` (int64): If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
* `trigger` (string): How this automation is triggered to run.
* `trigger_actions` (array(string)): If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
* `value` (object): A Hash of attributes specific to the automation type.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `automation` (string): Automation type


---

## Delete Automation

```
files_sdk.automation.delete(id)
```

### Parameters

* `id` (int64): Required - Automation ID.


---

## Manually Run Automation

```
automation = files_sdk.automation.find(id)
automation.manual_run()
```

### Parameters

* `id` (int64): Required - Automation ID.


---

## Update Automation

```
automation = files_sdk.automation.find(id)
automation.update({
  "source": "example",
  "destinations": ["folder_a/file_a.txt",{"folder_path":"folder_b","file_path":"file_b.txt"},{"folder_path":"folder_c"}],
  "destination_replace_from": "example",
  "destination_replace_to": "example",
  "interval": "year",
  "path": "example",
  "sync_ids": [1,2],
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule_days_of_week": [0,1,3],
  "schedule_times_of_day": ["7:30","11:30"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "always_overwrite_size_matching_files": True,
  "always_serialize_jobs": True,
  "description": "example",
  "disabled": True,
  "exclude_pattern": "path/to/exclude/*",
  "import_urls": [{"name":"users.json","url":"http://example.com/users","method":"POST","headers":{"Content-Type":"application/json"},"content":{"group":"support"}}],
  "flatten_destination_structure": True,
  "ignore_locked_folders": True,
  "legacy_folder_matching": False,
  "name": "example",
  "overwrite_files": True,
  "path_time_zone": "Eastern Time (US & Canada)",
  "retry_on_failure_interval_in_minutes": 60,
  "retry_on_failure_number_of_attempts": 10,
  "trigger": "daily",
  "trigger_actions": ["create"],
  "value": {"limit":"1"},
  "recurring_day": 25,
  "automation": "create_folder"
})
```

### Parameters

* `id` (int64): Required - Automation ID.
* `source` (string): Source path/glob.  See Automation docs for exact description, but this is used to filter for files in the `path` to find files to operate on. Supports globs, except on remote mounts.
* `destinations` (array(string)): A list of String destination paths or Hash of folder_path and optional file_path.
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs, except on remote mounts.
* `sync_ids` (string): A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`. A list of days of the week to run this automation. 0 is Sunday, 1 is Monday, etc.
* `schedule_times_of_day` (array(string)): If trigger is `custom_schedule`. A list of times of day to run this automation. 24-hour time format.
* `schedule_time_zone` (string): If trigger is `custom_schedule`. Time zone for the schedule.
* `always_overwrite_size_matching_files` (boolean): Ordinarily, files with identical size in the source and destination will be skipped from copy operations to prevent wasted transfer.  If this flag is `true` we will overwrite the destination file always.  Note that this may cause large amounts of wasted transfer usage.  This setting has no effect unless `overwrite_files` is also set to `true`.
* `always_serialize_jobs` (boolean): Ordinarily, we will allow automation runs to run in parallel for non-scheduled automations. If this flag is `true` we will force automation runs to be serialized (run one at a time, one after another). This can resolve some issues with race conditions on remote systems at the cost of some performance.
* `description` (string): Description for the this Automation.
* `disabled` (boolean): If true, this automation will not run.
* `exclude_pattern` (string): If set, this glob pattern will exclude files from the automation. Supports globs, except on remote mounts.
* `import_urls` (array(object)): List of URLs to be imported and names to be used.
* `flatten_destination_structure` (boolean): Normally copy and move automations that use globs will implicitly preserve the source folder structure in the destination.  If this flag is `true`, the source folder structure will be flattened in the destination.  This is useful for copying or moving files from multiple folders into a single destination folder.
* `ignore_locked_folders` (boolean): If true, the Lock Folders behavior will be disregarded for automated actions.
* `legacy_folder_matching` (boolean): DEPRECATED: If `true`, use the legacy behavior for this automation, where it can operate on folders in addition to just files.  This behavior no longer works and should not be used.
* `name` (string): Name for this automation.
* `overwrite_files` (boolean): If true, existing files will be overwritten with new files on Move/Copy automations.  Note: by default files will not be overwritten on Copy automations if they appear to be the same file size as the newly incoming file.  Use the `always_overwrite_size_matching_files` option in conjunction with `overwrite_files` to override this behavior and overwrite files no matter what.
* `path_time_zone` (string): Timezone to use when rendering timestamps in paths.
* `retry_on_failure_interval_in_minutes` (int64): If the Automation fails, retry at this interval (in minutes).  Acceptable values are 5 through 1440 (one day).  Set to null to disable.
* `retry_on_failure_number_of_attempts` (int64): If the Automation fails, retry at most this many times.  Maximum allowed value: 10.  Set to null to disable.
* `trigger` (string): How this automation is triggered to run.
* `trigger_actions` (array(string)): If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
* `value` (object): A Hash of attributes specific to the automation type.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `automation` (string): Automation type


---

## Delete Automation

```
automation = files_sdk.automation.find(id)
automation.delete()
```

### Parameters

* `id` (int64): Required - Automation ID.

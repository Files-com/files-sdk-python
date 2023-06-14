# Automation

## Example Automation Object

```
{
  "id": 1,
  "automation": "create_folder",
  "deleted": True,
  "disabled": True,
  "trigger": "realtime",
  "interval": "week",
  "last_modified_at": "2000-01-01T01:00:00Z",
  "name": "example",
  "schedule": "example",
  "source": "example",
  "destinations": [
    "destination"
  ],
  "destination_replace_from": "example",
  "destination_replace_to": "example",
  "description": "example",
  "recurring_day": 25,
  "path": "example",
  "user_id": 1,
  "sync_ids": [
    1,
    2
  ],
  "user_ids": [
    1,
    2
  ],
  "group_ids": [
    1,
    2
  ],
  "webhook_url": "https://app.files.com/api/webhooks/abc123",
  "trigger_actions": [
    "create"
  ],
  "value": {
    "limit": "1"
  }
}
```

* `id` (int64): Automation ID
* `automation` (string): Automation type
* `deleted` (boolean): Indicates if the automation has been deleted.
* `disabled` (boolean): If true, this automation will not run.
* `trigger` (string): How this automation is triggered to run. One of: `realtime`, `daily`, `custom_schedule`, `webhook`, `email`, or `action`.
* `interval` (string): If trigger is `daily`, this specifies how often to run this automation.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `last_modified_at` (date-time): Time when automation was last modified. Does not change for name or description updates.
* `name` (string): Name for this automation.
* `schedule` (object): If trigger is `custom_schedule`, Custom schedule description for when the automation should be run.
* `source` (string): Source Path
* `destinations` (array): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `description` (string): Description for the this Automation.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `path` (string): Path on which this Automation runs.  Supports globs. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `user_id` (int64): User ID of the Automation's creator.
* `sync_ids` (array): IDs of remote sync folder behaviors to run by this Automation
* `user_ids` (array): IDs of Users for the Automation (i.e. who to Request File from)
* `group_ids` (array): IDs of Groups for the Automation (i.e. who to Request File from)
* `webhook_url` (string): If trigger is `webhook`, this is the URL of the webhook to trigger the Automation.
* `trigger_actions` (array): If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
* `value` (object): A Hash of attributes specific to the automation type.
* `destination` (string): DEPRECATED: Destination Path. Use `destinations` instead.


---

## List Automations

```
files_sdk.automation.list({
  "per_page": 1,
  "with_deleted": True
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[automation]=desc`). Valid fields are `automation`, `disabled`, `last_modified_at` or `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `last_modified_at` or `automation`. Valid field combinations are `[ automation, disabled ]` and `[ disabled, automation ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `last_modified_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `last_modified_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `last_modified_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `last_modified_at`.
* `with_deleted` (boolean): Set to true to include deleted automations in the results.


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
  "source": "source",
  "destinations": ["folder_a/file_a.txt",{"folder_path":"folder_b","file_path":"file_b.txt"},{"folder_path":"folder_c"}],
  "destination_replace_from": "example",
  "destination_replace_to": "example",
  "interval": "year",
  "path": "example",
  "sync_ids": [1,2],
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule": {"days_of_week":[0,1,3],"times_of_day":["7:30","11:30"],"time_zone":"Eastern Time (US & Canada)"},
  "description": "example",
  "disabled": True,
  "name": "example",
  "trigger": "realtime",
  "trigger_actions": ["create"],
  "value": {"limit":"1"},
  "recurring_day": 25,
  "automation": "create_folder"
})
```

### Parameters

* `source` (string): Source Path
* `destination` (string): DEPRECATED: Destination Path. Use `destinations` instead.
* `destinations` (array(string)): A list of String destination paths or Hash of folder_path and optional file_path.
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `sync_ids` (string): A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule` (object): Custom schedule for running this automation.
* `description` (string): Description for the this Automation.
* `disabled` (boolean): If true, this automation will not run.
* `name` (string): Name for this automation.
* `trigger` (string): How this automation is triggered to run. One of: `realtime`, `daily`, `custom_schedule`, `webhook`, `email`, or `action`.
* `trigger_actions` (array(string)): If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
* `value` (object): A Hash of attributes specific to the automation type.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `automation` (string): Required - Automation type


---

## Update Automation

```
files_sdk.automation.update(id, {
  "source": "source",
  "destinations": ["folder_a/file_a.txt",{"folder_path":"folder_b","file_path":"file_b.txt"},{"folder_path":"folder_c"}],
  "destination_replace_from": "example",
  "destination_replace_to": "example",
  "interval": "year",
  "path": "example",
  "sync_ids": [1,2],
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule": {"days_of_week":[0,1,3],"times_of_day":["7:30","11:30"],"time_zone":"Eastern Time (US & Canada)"},
  "description": "example",
  "disabled": True,
  "name": "example",
  "trigger": "realtime",
  "trigger_actions": ["create"],
  "value": {"limit":"1"},
  "recurring_day": 25,
  "automation": "create_folder"
})
```

### Parameters

* `id` (int64): Required - Automation ID.
* `source` (string): Source Path
* `destination` (string): DEPRECATED: Destination Path. Use `destinations` instead.
* `destinations` (array(string)): A list of String destination paths or Hash of folder_path and optional file_path.
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `sync_ids` (string): A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule` (object): Custom schedule for running this automation.
* `description` (string): Description for the this Automation.
* `disabled` (boolean): If true, this automation will not run.
* `name` (string): Name for this automation.
* `trigger` (string): How this automation is triggered to run. One of: `realtime`, `daily`, `custom_schedule`, `webhook`, `email`, or `action`.
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

## Update Automation

```
automation = files_sdk.automation.list.first
automation.update({
  "source": "source",
  "destinations": ["folder_a/file_a.txt",{"folder_path":"folder_b","file_path":"file_b.txt"},{"folder_path":"folder_c"}],
  "destination_replace_from": "example",
  "destination_replace_to": "example",
  "interval": "year",
  "path": "example",
  "sync_ids": [1,2],
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule": {"days_of_week":[0,1,3],"times_of_day":["7:30","11:30"],"time_zone":"Eastern Time (US & Canada)"},
  "description": "example",
  "disabled": True,
  "name": "example",
  "trigger": "realtime",
  "trigger_actions": ["create"],
  "value": {"limit":"1"},
  "recurring_day": 25,
  "automation": "create_folder"
})
```

### Parameters

* `id` (int64): Required - Automation ID.
* `source` (string): Source Path
* `destination` (string): DEPRECATED: Destination Path. Use `destinations` instead.
* `destinations` (array(string)): A list of String destination paths or Hash of folder_path and optional file_path.
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `sync_ids` (string): A list of sync IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule` (object): Custom schedule for running this automation.
* `description` (string): Description for the this Automation.
* `disabled` (boolean): If true, this automation will not run.
* `name` (string): Name for this automation.
* `trigger` (string): How this automation is triggered to run. One of: `realtime`, `daily`, `custom_schedule`, `webhook`, `email`, or `action`.
* `trigger_actions` (array(string)): If trigger is `action`, this is the list of action types on which to trigger the automation. Valid actions are create, read, update, destroy, move, copy
* `value` (object): A Hash of attributes specific to the automation type.
* `recurring_day` (int64): If trigger type is `daily`, this specifies a day number to run in one of the supported intervals: `week`, `month`, `quarter`, `year`.
* `automation` (string): Automation type


---

## Delete Automation

```
automation = files_sdk.automation.list.first
automation.delete()
```

### Parameters

* `id` (int64): Required - Automation ID.

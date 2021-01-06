# Automation

## Example Automation Object

```
{
  "id": 1,
  "automation": "create_folder",
  "trigger": "realtime",
  "interval": "week",
  "next_process_on": "2020-01-01",
  "schedule": {
    "days_of_week": [
      0,
      2,
      4
    ],
    "times_of_day": [
      "6:30",
      "14:30"
    ],
    "time_zone": "Eastern Time (US & Canada)"
  },
  "source": "",
  "destination": "",
  "destination_replace_from": "",
  "destination_replace_to": "",
  "path": "",
  "user_id": 1,
  "user_ids": [
    1,
    2
  ],
  "group_ids": [
    1,
    2
  ],
  "webhook_url": "https://app.files.com/api/webhooks/abc123"
}
```

* `id` (int64): Automation ID
* `automation` (string): Automation type
* `trigger` (string): How this automation is triggered to run. One of: `realtime`, `daily`, `custom_schedule`, `webhook`, or `email`.
* `interval` (string): If trigger is `daily`, this specifies how often to run this automation.  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `next_process_on` (string): If trigger is `daily`, date this automation will next run.
* `schedule` (object): If trigger is `custom_schedule`, Custom schedule description for when the automation should be run.
* `source` (string): Source Path
* `destination` (string): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `path` (string): Path on which this Automation runs.  Supports globs. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `user_id` (int64): User ID of the Automation's creator.
* `user_ids` (array): IDs of Users for the Automation (i.e. who to Request File from)
* `group_ids` (array): IDs of Groups for the Automation (i.e. who to Request File from)
* `webhook_url` (string): If trigger is `webhook`, this is the URL of the webhook to trigger the Automation.


---

## List Automations

```
files_sdk.automation.list({
  "per_page": 1,
  "automation": "create_folder"
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `automation`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `automation`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `automation`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `automation`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `automation`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `automation`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `automation`.
* `automation` (string): DEPRECATED: Type of automation to filter by. Use `filter[automation]` instead.


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
  "automation": "create_folder",
  "source": "source",
  "destination": "destination",
  "interval": "year",
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule": "{\"days_of_week\": [ 0, 1, 3 ], \"times_of_day\": [ \"7:30\", \"11:30\" ], \"time_zone\": \"Eastern Time (US & Canada)\"}",
  "trigger": "realtime"
})
```

### Parameters

* `automation` (string): Required - Automation type
* `source` (string): Source Path
* `destination` (string): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule` (object): Custom schedule for running this automation.
* `trigger` (string): How this automation is triggered to run. One of: `realtime`, `daily`, `custom_schedule`, `webhook`, or `email`.


---

## Update Automation

```
files_sdk.automation.update(id, {
  "automation": "create_folder",
  "source": "source",
  "destination": "destination",
  "interval": "year",
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule": "{\"days_of_week\": [ 0, 1, 3 ], \"times_of_day\": [ \"7:30\", \"11:30\" ], \"time_zone\": \"Eastern Time (US & Canada)\"}",
  "trigger": "realtime"
})
```

### Parameters

* `id` (int64): Required - Automation ID.
* `automation` (string): Required - Automation type
* `source` (string): Source Path
* `destination` (string): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule` (object): Custom schedule for running this automation.
* `trigger` (string): How this automation is triggered to run. One of: `realtime`, `daily`, `custom_schedule`, `webhook`, or `email`.


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
automation = files_sdk.automation.find(1)

automation.update({
  "automation": "create_folder",
  "source": "source",
  "destination": "destination",
  "interval": "year",
  "user_ids": [1,2],
  "group_ids": [1,2],
  "schedule": "{\"days_of_week\": [ 0, 1, 3 ], \"times_of_day\": [ \"7:30\", \"11:30\" ], \"time_zone\": \"Eastern Time (US & Canada)\"}",
  "trigger": "realtime"
})
```

### Parameters

* `id` (int64): Required - Automation ID.
* `automation` (string): Required - Automation type
* `source` (string): Source Path
* `destination` (string): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `schedule` (object): Custom schedule for running this automation.
* `trigger` (string): How this automation is triggered to run. One of: `realtime`, `daily`, `custom_schedule`, `webhook`, or `email`.


---

## Delete Automation

```
automation = files_sdk.automation.find(1)

automation.delete()
```

### Parameters

* `id` (int64): Required - Automation ID.

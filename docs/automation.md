# Automation

## Example Automation Object

```
{
  "id": 1,
  "automation": "create_folder",
  "source": "",
  "destination": "",
  "destination_replace_from": "",
  "destination_replace_to": "",
  "interval": "week",
  "next_process_on": "2020-01-01",
  "path": "",
  "realtime": True,
  "user_id": 1,
  "user_ids": [

  ],
  "group_ids": [

  ]
}
```

* `id` (int64): Automation ID
* `automation` (string): Automation type
* `source` (string): Source Path
* `destination` (string): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation?  One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `next_process_on` (string): Date this automation will next run.
* `path` (string): Path on which this Automation runs.  Supports globs. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `realtime` (boolean): Does this automation run in real time?  This is a read-only property based on automation type.
* `user_id` (int64): User ID of the Automation's creator.
* `user_ids` (array): IDs of Users for the Automation (i.e. who to Request File from)
* `group_ids` (array): IDs of Groups for the Automation (i.e. who to Request File from)


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
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `site_id` and `automation`.
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
  "interval": "year"
})
```

### Parameters

* `automation` (string): Required - Type of automation.  One of: `create_folder`, `request_file`, `request_move`
* `source` (string): Source Path
* `destination` (string): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.


---

## Update Automation

```
files_sdk.automation.update(id, {
  "automation": "create_folder",
  "source": "source",
  "destination": "destination",
  "interval": "year"
})
```

### Parameters

* `id` (int64): Required - Automation ID.
* `automation` (string): Required - Type of automation.  One of: `create_folder`, `request_file`, `request_move`
* `source` (string): Source Path
* `destination` (string): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.


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
  "interval": "year"
})
```

### Parameters

* `id` (int64): Required - Automation ID.
* `automation` (string): Required - Type of automation.  One of: `create_folder`, `request_file`, `request_move`
* `source` (string): Source Path
* `destination` (string): Destination Path
* `destination_replace_from` (string): If set, this string in the destination path will be replaced with the value in `destination_replace_to`.
* `destination_replace_to` (string): If set, this string will replace the value `destination_replace_from` in the destination filename. You can use special patterns here.
* `interval` (string): How often to run this automation? One of: `day`, `week`, `week_end`, `month`, `month_end`, `quarter`, `quarter_end`, `year`, `year_end`
* `path` (string): Path on which this Automation runs.  Supports globs.
* `user_ids` (string): A list of user IDs the automation is associated with. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs the automation is associated with. If sent as a string, it should be comma-delimited.


---

## Delete Automation

```
automation = files_sdk.automation.find(1)

automation.delete()
```

### Parameters

* `id` (int64): Required - Automation ID.

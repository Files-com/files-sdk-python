# ScheduledExport

## Example ScheduledExport Object

```
{
  "id": 1,
  "name": "Monthly access review",
  "export_type": "permission_audit",
  "report_name": "Permission audit",
  "export_options": {
    "group_by": "user"
  },
  "user_id": 1,
  "disabled": True,
  "trigger": "daily",
  "interval": "month",
  "recurring_day": 1,
  "schedule_days_of_week": [
    1,
    3,
    5
  ],
  "schedule_times_of_day": [
    "06:30"
  ],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us",
  "human_readable_schedule": "Runs every month at 06:30 AM UTC TZ.",
  "last_run_at": "2000-01-01T01:00:00Z",
  "last_export_id": 1,
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Scheduled Export ID
* `name` (string): Name for this scheduled export.
* `export_type` (string): Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
* `report_name` (string): Human-readable report name.
* `export_options` (object): Report-specific options. `permission_audit` supports `group_by` with `user` or `path`.
* `user_id` (int64): Site Admin user who receives the completed export e-mail.
* `disabled` (boolean): If true, this scheduled export will not run.
* `trigger` (string): Schedule trigger type: `daily` or `custom_schedule`.
* `interval` (string): If trigger is `daily`, this specifies how often to run the scheduled export.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for schedule-driven exports.
* `schedule_time_zone` (string): Time zone used by the scheduled export.
* `holiday_region` (string): Optional holiday region used by schedule-driven exports.
* `human_readable_schedule` (string): Human-readable schedule description.
* `last_run_at` (date-time): Most recent scheduled run time.
* `last_export_id` (int64): Most recent Export ID created by this schedule.
* `created_at` (date-time): Creation time.
* `updated_at` (date-time): Last update time.


---

## List Scheduled Exports

```
files_sdk.scheduled_export.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `export_type` or `disabled`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `export_type`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `export_type`.


---

## Show Scheduled Export

```
files_sdk.scheduled_export.find(id)
```

### Parameters

* `id` (int64): Required - Scheduled Export ID.


---

## Create Scheduled Export

```
files_sdk.scheduled_export.create({
  "name": "Monthly access review",
  "export_type": "permission_audit",
  "export_options": {"group_by":"user"},
  "user_id": 1,
  "disabled": True,
  "trigger": "daily",
  "interval": "month",
  "recurring_day": 1,
  "schedule_days_of_week": [1,3,5],
  "schedule_times_of_day": ["06:30"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us"
})
```

### Parameters

* `name` (string): Required - Name for this scheduled export.
* `export_type` (string): Required - Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
* `export_options` (object): Report-specific options. `permission_audit` supports `group_by` with `user` or `path`.
* `user_id` (int64): Site Admin user who receives the completed export e-mail.
* `disabled` (boolean): If true, this scheduled export will not run.
* `trigger` (string): Schedule trigger type: `daily` or `custom_schedule`.
* `interval` (string): If trigger is `daily`, this specifies how often to run the scheduled export.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for schedule-driven exports.
* `schedule_time_zone` (string): Time zone used by the scheduled export.
* `holiday_region` (string): Optional holiday region used by schedule-driven exports.


---

## Create an export CSV of Scheduled Export resources

```
files_sdk.scheduled_export.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `export_type` or `disabled`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `export_type`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `export_type`.


---

## Update Scheduled Export

```
files_sdk.scheduled_export.update(id, {
  "name": "Monthly access review",
  "export_type": "permission_audit",
  "export_options": {"group_by":"user"},
  "user_id": 1,
  "disabled": True,
  "trigger": "daily",
  "interval": "month",
  "recurring_day": 1,
  "schedule_days_of_week": [1,3,5],
  "schedule_times_of_day": ["06:30"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us"
})
```

### Parameters

* `id` (int64): Required - Scheduled Export ID.
* `name` (string): Name for this scheduled export.
* `export_type` (string): Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
* `export_options` (object): Report-specific options. `permission_audit` supports `group_by` with `user` or `path`.
* `user_id` (int64): Site Admin user who receives the completed export e-mail.
* `disabled` (boolean): If true, this scheduled export will not run.
* `trigger` (string): Schedule trigger type: `daily` or `custom_schedule`.
* `interval` (string): If trigger is `daily`, this specifies how often to run the scheduled export.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for schedule-driven exports.
* `schedule_time_zone` (string): Time zone used by the scheduled export.
* `holiday_region` (string): Optional holiday region used by schedule-driven exports.


---

## Delete Scheduled Export

```
files_sdk.scheduled_export.delete(id)
```

### Parameters

* `id` (int64): Required - Scheduled Export ID.


---

## Update Scheduled Export

```
scheduled_export = files_sdk.scheduled_export.find(id)
scheduled_export.update({
  "name": "Monthly access review",
  "export_type": "permission_audit",
  "export_options": {"group_by":"user"},
  "user_id": 1,
  "disabled": True,
  "trigger": "daily",
  "interval": "month",
  "recurring_day": 1,
  "schedule_days_of_week": [1,3,5],
  "schedule_times_of_day": ["06:30"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us"
})
```

### Parameters

* `id` (int64): Required - Scheduled Export ID.
* `name` (string): Name for this scheduled export.
* `export_type` (string): Export report type. Valid values: folder_size_audit, group_membership_audit, permission_audit, share_link_audit
* `export_options` (object): Report-specific options. `permission_audit` supports `group_by` with `user` or `path`.
* `user_id` (int64): Site Admin user who receives the completed export e-mail.
* `disabled` (boolean): If true, this scheduled export will not run.
* `trigger` (string): Schedule trigger type: `daily` or `custom_schedule`.
* `interval` (string): If trigger is `daily`, this specifies how often to run the scheduled export.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for schedule-driven exports.
* `schedule_time_zone` (string): Time zone used by the scheduled export.
* `holiday_region` (string): Optional holiday region used by schedule-driven exports.


---

## Delete Scheduled Export

```
scheduled_export = files_sdk.scheduled_export.find(id)
scheduled_export.delete()
```

### Parameters

* `id` (int64): Required - Scheduled Export ID.

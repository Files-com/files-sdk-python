# Schedule

## Example Schedule Object

```
{
  "id": 1,
  "name": "Weekday overnight",
  "schedule_days_of_week": [
    1,
    2,
    3,
    4,
    5
  ],
  "schedule_times_of_day": [
    "01:00"
  ],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us",
  "human_readable_schedule": "Triggered every Monday, Tuesday, Wednesday, Thursday, Friday at 01:00 AM UTC TZ.",
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Schedule ID.
* `name` (string): Schedule name.
* `schedule_days_of_week` (array(int64)): 0-based weekdays used by the Schedule. 0 is Sunday.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format (24-hour).
* `schedule_time_zone` (string): Time zone for scheduled times. If not set, times are interpreted as UTC.
* `holiday_region` (string): Optional holiday region on which linked resources do not run.
* `human_readable_schedule` (string): Human-readable Schedule description.
* `created_at` (date-time): Creation time.
* `updated_at` (date-time): Last update time.


---

## List Schedules

```
files_sdk.schedule.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`.


---

## Show Schedule

```
files_sdk.schedule.find(id)
```

### Parameters

* `id` (int64): Required - Schedule ID.


---

## Create Schedule

```
files_sdk.schedule.create({
  "name": "Weekday overnight",
  "schedule_days_of_week": [1,2,3,4,5],
  "schedule_times_of_day": ["01:00"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us"
})
```

### Parameters

* `name` (string): Required - Schedule name.
* `schedule_days_of_week` (array(int64)): Required - 0-based weekdays used by the Schedule. 0 is Sunday.
* `schedule_times_of_day` (array(string)): Required - Times of day in HH:MM format (24-hour).
* `schedule_time_zone` (string): Time zone for scheduled times. If not set, times are interpreted as UTC.
* `holiday_region` (string): Optional holiday region on which linked resources do not run.


---

## Update Schedule

```
files_sdk.schedule.update(id, {
  "name": "Weekday overnight",
  "schedule_days_of_week": [1,2,3,4,5],
  "schedule_times_of_day": ["01:00"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us"
})
```

### Parameters

* `id` (int64): Required - Schedule ID.
* `name` (string): Schedule name.
* `schedule_days_of_week` (array(int64)): 0-based weekdays used by the Schedule. 0 is Sunday.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format (24-hour).
* `schedule_time_zone` (string): Time zone for scheduled times. If not set, times are interpreted as UTC.
* `holiday_region` (string): Optional holiday region on which linked resources do not run.


---

## Delete Schedule

```
files_sdk.schedule.delete(id)
```

### Parameters

* `id` (int64): Required - Schedule ID.


---

## Update Schedule

```
schedule = files_sdk.schedule.find(id)
schedule.update({
  "name": "Weekday overnight",
  "schedule_days_of_week": [1,2,3,4,5],
  "schedule_times_of_day": ["01:00"],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "holiday_region": "us"
})
```

### Parameters

* `id` (int64): Required - Schedule ID.
* `name` (string): Schedule name.
* `schedule_days_of_week` (array(int64)): 0-based weekdays used by the Schedule. 0 is Sunday.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format (24-hour).
* `schedule_time_zone` (string): Time zone for scheduled times. If not set, times are interpreted as UTC.
* `holiday_region` (string): Optional holiday region on which linked resources do not run.


---

## Delete Schedule

```
schedule = files_sdk.schedule.find(id)
schedule.delete()
```

### Parameters

* `id` (int64): Required - Schedule ID.

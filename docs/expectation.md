# Expectation

## Example Expectation Object

```
{
  "id": 1,
  "workspace_id": 1,
  "name": "Daily Vendor Feed",
  "description": "Wait for the vendor CSV every morning.",
  "path": "incoming/vendor_a",
  "source": "*.csv",
  "exclude_pattern": "*.tmp",
  "disabled": True,
  "expectations_version": 1,
  "trigger": "manual",
  "interval": "day",
  "recurring_day": 3,
  "schedule_days_of_week": [
    1,
    3,
    5
  ],
  "schedule_times_of_day": [
    "06:00"
  ],
  "schedule_time_zone": "UTC",
  "holiday_region": "us",
  "lookback_interval": 3600,
  "late_acceptance_interval": 900,
  "inactivity_interval": 300,
  "max_open_interval": 43200,
  "criteria": {
    "count": {
      "exact": 1
    },
    "extensions": [
      "csv"
    ]
  },
  "last_evaluated_at": "2000-01-01T01:00:00Z",
  "last_success_at": "2000-01-01T01:00:00Z",
  "last_failure_at": "2000-01-01T01:00:00Z",
  "last_result": "success",
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Expectation ID
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.
* `name` (string): Expectation name.
* `description` (string): Expectation description.
* `path` (string): Path scope for the expectation. Supports workspace-relative presentation. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `source` (string): Source glob used to select candidate files.
* `exclude_pattern` (string): Optional source exclusion glob.
* `disabled` (boolean): If true, the expectation is disabled.
* `expectations_version` (int64): Criteria schema version for this expectation.
* `trigger` (string): How this expectation opens windows.
* `interval` (string): If trigger is `daily`, this specifies how often to run the expectation.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for schedule-driven expectations.
* `schedule_time_zone` (string): Time zone used by the expectation schedule.
* `holiday_region` (string): Optional holiday region used by schedule-driven expectations.
* `lookback_interval` (int64): How many seconds before the due boundary the window starts.
* `late_acceptance_interval` (int64): How many seconds a schedule-driven window may remain eligible to close as late.
* `inactivity_interval` (int64): How many quiet seconds are required before final closure.
* `max_open_interval` (int64): Hard-stop duration in seconds for unscheduled expectations.
* `criteria` (object): Structured criteria v1 definition for the expectation.
* `last_evaluated_at` (date-time): Last time this expectation was evaluated.
* `last_success_at` (date-time): Last time this expectation closed successfully.
* `last_failure_at` (date-time): Last time this expectation closed with a failure result.
* `last_result` (string): Most recent terminal result for this expectation.
* `created_at` (date-time): Creation time.
* `updated_at` (date-time): Last update time.


---

## List Expectations

```
files_sdk.expectation.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `name` or `disabled`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled` and `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.


---

## Show Expectation

```
files_sdk.expectation.find(id)
```

### Parameters

* `id` (int64): Required - Expectation ID.


---

## Create Expectation

```
files_sdk.expectation.create({
  "name": "Daily Vendor Feed",
  "description": "Wait for the vendor CSV every morning.",
  "path": "incoming/vendor_a",
  "source": "*.csv",
  "exclude_pattern": "*.tmp",
  "disabled": True,
  "trigger": "manual",
  "interval": "day",
  "recurring_day": 3,
  "schedule_days_of_week": [1,3,5],
  "schedule_times_of_day": ["06:00"],
  "schedule_time_zone": "UTC",
  "holiday_region": "us",
  "lookback_interval": 3600,
  "late_acceptance_interval": 900,
  "inactivity_interval": 300,
  "max_open_interval": 43200,
  "criteria": {"count":{"exact":1},"extensions":["csv"]},
  "workspace_id": 0
})
```

### Parameters

* `name` (string): Expectation name.
* `description` (string): Expectation description.
* `path` (string): Path scope for the expectation. Supports workspace-relative presentation.
* `source` (string): Source glob used to select candidate files.
* `exclude_pattern` (string): Optional source exclusion glob.
* `disabled` (boolean): If true, the expectation is disabled.
* `trigger` (string): How this expectation opens windows.
* `interval` (string): If trigger is `daily`, this specifies how often to run the expectation.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for schedule-driven expectations.
* `schedule_time_zone` (string): Time zone used by the expectation schedule.
* `holiday_region` (string): Optional holiday region used by schedule-driven expectations.
* `lookback_interval` (int64): How many seconds before the due boundary the window starts.
* `late_acceptance_interval` (int64): How many seconds a schedule-driven window may remain eligible to close as late.
* `inactivity_interval` (int64): How many quiet seconds are required before final closure.
* `max_open_interval` (int64): Hard-stop duration in seconds for unscheduled expectations.
* `criteria` (object): Structured criteria v1 definition for the expectation.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Manually open an Expectation window

```
files_sdk.expectation.trigger(id)
```

### Parameters

* `id` (int64): Required - Expectation ID.


---

## Update Expectation

```
files_sdk.expectation.update(id, {
  "name": "Daily Vendor Feed",
  "description": "Wait for the vendor CSV every morning.",
  "path": "incoming/vendor_a",
  "source": "*.csv",
  "exclude_pattern": "*.tmp",
  "disabled": True,
  "trigger": "manual",
  "interval": "day",
  "recurring_day": 3,
  "schedule_days_of_week": [1,3,5],
  "schedule_times_of_day": ["06:00"],
  "schedule_time_zone": "UTC",
  "holiday_region": "us",
  "lookback_interval": 3600,
  "late_acceptance_interval": 900,
  "inactivity_interval": 300,
  "max_open_interval": 43200,
  "criteria": {"count":{"exact":1},"extensions":["csv"]},
  "workspace_id": 0
})
```

### Parameters

* `id` (int64): Required - Expectation ID.
* `name` (string): Expectation name.
* `description` (string): Expectation description.
* `path` (string): Path scope for the expectation. Supports workspace-relative presentation.
* `source` (string): Source glob used to select candidate files.
* `exclude_pattern` (string): Optional source exclusion glob.
* `disabled` (boolean): If true, the expectation is disabled.
* `trigger` (string): How this expectation opens windows.
* `interval` (string): If trigger is `daily`, this specifies how often to run the expectation.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for schedule-driven expectations.
* `schedule_time_zone` (string): Time zone used by the expectation schedule.
* `holiday_region` (string): Optional holiday region used by schedule-driven expectations.
* `lookback_interval` (int64): How many seconds before the due boundary the window starts.
* `late_acceptance_interval` (int64): How many seconds a schedule-driven window may remain eligible to close as late.
* `inactivity_interval` (int64): How many quiet seconds are required before final closure.
* `max_open_interval` (int64): Hard-stop duration in seconds for unscheduled expectations.
* `criteria` (object): Structured criteria v1 definition for the expectation.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Delete Expectation

```
files_sdk.expectation.delete(id)
```

### Parameters

* `id` (int64): Required - Expectation ID.


---

## Manually open an Expectation window

```
expectation = files_sdk.expectation.find(id)
expectation.trigger()
```

### Parameters

* `id` (int64): Required - Expectation ID.


---

## Update Expectation

```
expectation = files_sdk.expectation.find(id)
expectation.update({
  "name": "Daily Vendor Feed",
  "description": "Wait for the vendor CSV every morning.",
  "path": "incoming/vendor_a",
  "source": "*.csv",
  "exclude_pattern": "*.tmp",
  "disabled": True,
  "trigger": "manual",
  "interval": "day",
  "recurring_day": 3,
  "schedule_days_of_week": [1,3,5],
  "schedule_times_of_day": ["06:00"],
  "schedule_time_zone": "UTC",
  "holiday_region": "us",
  "lookback_interval": 3600,
  "late_acceptance_interval": 900,
  "inactivity_interval": 300,
  "max_open_interval": 43200,
  "criteria": {"count":{"exact":1},"extensions":["csv"]},
  "workspace_id": 0
})
```

### Parameters

* `id` (int64): Required - Expectation ID.
* `name` (string): Expectation name.
* `description` (string): Expectation description.
* `path` (string): Path scope for the expectation. Supports workspace-relative presentation.
* `source` (string): Source glob used to select candidate files.
* `exclude_pattern` (string): Optional source exclusion glob.
* `disabled` (boolean): If true, the expectation is disabled.
* `trigger` (string): How this expectation opens windows.
* `interval` (string): If trigger is `daily`, this specifies how often to run the expectation.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for schedule-driven expectations.
* `schedule_time_zone` (string): Time zone used by the expectation schedule.
* `holiday_region` (string): Optional holiday region used by schedule-driven expectations.
* `lookback_interval` (int64): How many seconds before the due boundary the window starts.
* `late_acceptance_interval` (int64): How many seconds a schedule-driven window may remain eligible to close as late.
* `inactivity_interval` (int64): How many quiet seconds are required before final closure.
* `max_open_interval` (int64): Hard-stop duration in seconds for unscheduled expectations.
* `criteria` (object): Structured criteria v1 definition for the expectation.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Delete Expectation

```
expectation = files_sdk.expectation.find(id)
expectation.delete()
```

### Parameters

* `id` (int64): Required - Expectation ID.

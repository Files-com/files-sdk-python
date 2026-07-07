# AiTask

## Example AiTask Object

```
{
  "id": 1,
  "workspace_id": 1,
  "name": "Summarize daily reports",
  "description": "Summarizes files uploaded by the accounting team.",
  "prompt": "Summarize the uploaded file and identify follow-up actions.",
  "permission_set": "files_only",
  "path": "incoming/reports",
  "source": "*.pdf",
  "disabled": True,
  "trigger": "daily",
  "trigger_actions": [
    "create"
  ],
  "interval": "day",
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
  "human_readable_schedule": "Runs every day at 06:30 AM UTC TZ.",
  "last_run_at": "2000-01-01T01:00:00Z",
  "master_admin_user_id": 1,
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): AI Task ID.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.
* `name` (string): AI Task name.
* `description` (string): AI Task description.
* `prompt` (string): Prompt sent when this AI Task is invoked.
* `permission_set` (string): Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
* `path` (string): Path scope used for action-triggered AI Tasks. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `source` (string): Source glob used with `path` for action-triggered AI Tasks.
* `disabled` (boolean): If true, this AI Task will not run.
* `trigger` (string): How this AI Task is triggered.
* `trigger_actions` (array(string)): If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
* `interval` (string): If trigger is `daily`, this specifies how often to run the AI Task.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for scheduled AI Tasks.
* `schedule_time_zone` (string): Time zone used by the AI Task schedule.
* `holiday_region` (string): Optional holiday region used by scheduled AI Tasks.
* `human_readable_schedule` (string): Human-readable schedule description.
* `last_run_at` (date-time): Most recent successful invocation time.
* `master_admin_user_id` (int64): Master User ID used for AI Task invocations.
* `created_at` (date-time): Creation time.
* `updated_at` (date-time): Last update time.


---

## List Ai Tasks

```
files_sdk.ai_task.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `id`, `disabled` or `updated_at`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `trigger` or `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.


---

## Show Ai Task

```
files_sdk.ai_task.find(id)
```

### Parameters

* `id` (int64): Required - Ai Task ID.


---

## Create Ai Task

```
files_sdk.ai_task.create({
  "description": "Summarizes files uploaded by the accounting team.",
  "disabled": True,
  "holiday_region": "us",
  "interval": "day",
  "name": "Summarize daily reports",
  "path": "incoming/reports",
  "permission_set": "files_only",
  "prompt": "Summarize the uploaded file and identify follow-up actions.",
  "recurring_day": 1,
  "schedule_days_of_week": [1,3,5],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "schedule_times_of_day": ["06:30"],
  "source": "*.pdf",
  "trigger": "daily",
  "trigger_actions": ["create"],
  "workspace_id": 0
})
```

### Parameters

* `description` (string): AI Task description.
* `disabled` (boolean): If true, this AI Task will not run.
* `holiday_region` (string): Optional holiday region used by scheduled AI Tasks.
* `interval` (string): If trigger is `daily`, this specifies how often to run the AI Task.
* `name` (string): Required - AI Task name.
* `path` (string): Path scope used for action-triggered AI Tasks.
* `permission_set` (string): Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
* `prompt` (string): Required - Prompt sent when this AI Task is invoked.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_time_zone` (string): Time zone used by the AI Task schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for scheduled AI Tasks.
* `source` (string): Source glob used with `path` for action-triggered AI Tasks.
* `trigger` (string): How this AI Task is triggered.
* `trigger_actions` (array(string)): If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Manually Run AI Task

```
files_sdk.ai_task.manual_run(id)
```

### Parameters

* `id` (int64): Required - Ai Task ID.


---

## Create an export CSV of Ai Task resources

```
files_sdk.ai_task.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `id`, `disabled` or `updated_at`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `disabled`, `trigger` or `workspace_id`. Valid field combinations are `[ workspace_id, disabled ]`.


---

## Update Ai Task

```
files_sdk.ai_task.update(id, {
  "description": "Summarizes files uploaded by the accounting team.",
  "disabled": True,
  "holiday_region": "us",
  "interval": "day",
  "name": "Summarize daily reports",
  "path": "incoming/reports",
  "permission_set": "files_only",
  "prompt": "Summarize the uploaded file and identify follow-up actions.",
  "recurring_day": 1,
  "schedule_days_of_week": [1,3,5],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "schedule_times_of_day": ["06:30"],
  "source": "*.pdf",
  "trigger": "daily",
  "trigger_actions": ["create"],
  "workspace_id": 0
})
```

### Parameters

* `id` (int64): Required - Ai Task ID.
* `description` (string): AI Task description.
* `disabled` (boolean): If true, this AI Task will not run.
* `holiday_region` (string): Optional holiday region used by scheduled AI Tasks.
* `interval` (string): If trigger is `daily`, this specifies how often to run the AI Task.
* `name` (string): AI Task name.
* `path` (string): Path scope used for action-triggered AI Tasks.
* `permission_set` (string): Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
* `prompt` (string): Prompt sent when this AI Task is invoked.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_time_zone` (string): Time zone used by the AI Task schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for scheduled AI Tasks.
* `source` (string): Source glob used with `path` for action-triggered AI Tasks.
* `trigger` (string): How this AI Task is triggered.
* `trigger_actions` (array(string)): If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Delete Ai Task

```
files_sdk.ai_task.delete(id)
```

### Parameters

* `id` (int64): Required - Ai Task ID.


---

## Manually Run AI Task

```
ai_task = files_sdk.ai_task.find(id)
ai_task.manual_run()
```

### Parameters

* `id` (int64): Required - Ai Task ID.


---

## Update Ai Task

```
ai_task = files_sdk.ai_task.find(id)
ai_task.update({
  "description": "Summarizes files uploaded by the accounting team.",
  "disabled": True,
  "holiday_region": "us",
  "interval": "day",
  "name": "Summarize daily reports",
  "path": "incoming/reports",
  "permission_set": "files_only",
  "prompt": "Summarize the uploaded file and identify follow-up actions.",
  "recurring_day": 1,
  "schedule_days_of_week": [1,3,5],
  "schedule_time_zone": "Eastern Time (US & Canada)",
  "schedule_times_of_day": ["06:30"],
  "source": "*.pdf",
  "trigger": "daily",
  "trigger_actions": ["create"],
  "workspace_id": 0
})
```

### Parameters

* `id` (int64): Required - Ai Task ID.
* `description` (string): AI Task description.
* `disabled` (boolean): If true, this AI Task will not run.
* `holiday_region` (string): Optional holiday region used by scheduled AI Tasks.
* `interval` (string): If trigger is `daily`, this specifies how often to run the AI Task.
* `name` (string): AI Task name.
* `path` (string): Path scope used for action-triggered AI Tasks.
* `permission_set` (string): Permissions used by the internal API key for this AI Task. Valid values are `full` and `files_only`.
* `prompt` (string): Prompt sent when this AI Task is invoked.
* `recurring_day` (int64): If trigger is `daily`, this selects the day number inside the chosen interval.
* `schedule_days_of_week` (array(int64)): If trigger is `custom_schedule`, the 0-based weekdays used by the schedule.
* `schedule_time_zone` (string): Time zone used by the AI Task schedule.
* `schedule_times_of_day` (array(string)): Times of day in HH:MM format for scheduled AI Tasks.
* `source` (string): Source glob used with `path` for action-triggered AI Tasks.
* `trigger` (string): How this AI Task is triggered.
* `trigger_actions` (array(string)): If trigger is `action`, the file action types that invoke this AI Task. Valid actions are create, copy, move, archived_delete, update, read, destroy.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Delete Ai Task

```
ai_task = files_sdk.ai_task.find(id)
ai_task.delete()
```

### Parameters

* `id` (int64): Required - Ai Task ID.

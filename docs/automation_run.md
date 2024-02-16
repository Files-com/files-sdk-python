# AutomationRun

## Example AutomationRun Object

```
{
  "id": 1,
  "automation_id": 1,
  "completed_at": "2000-01-01T01:00:00Z",
  "created_at": "2000-01-01T01:00:00Z",
  "runtime": "2000-01-01T01:00:00Z",
  "status": "success",
  "run_stage": "planning",
  "successful_operations": 1,
  "failed_operations": 1,
  "status_messages_url": "https://www.example.com/log_file.txt"
}
```

* `id` (int64): ID.
* `automation_id` (int64): ID of the associated Automation.
* `completed_at` (date-time): Automation run completion/failure date/time.
* `created_at` (date-time): Automation run start date/time.
* `runtime` (date-time): Automation run runtime.
* `status` (string): The success status of the AutomationRun. One of `running`, `success`, `partial_failure`, or `failure`.
* `run_stage` (string): The stage currently being executed in the execution environment.  One of `queued_for_planning`, `planning`, `queued_for_execution`, `executing`, or `finished`.
* `successful_operations` (int64): Count of successful operations.
* `failed_operations` (int64): Count of failed operations.
* `status_messages_url` (string): Link to status messages log file.


---

## List Automation Runs

```
files_sdk.automation_run.list({
  "per_page": 1,
  "automation_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[automation_id]=desc`). Valid fields are `automation_id`, `created_at` or `status`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `status` and `automation_id`. Valid field combinations are `[ automation_id, status ]`.
* `automation_id` (int64): Required - ID of the associated Automation.


---

## Show Automation Run

```
files_sdk.automation_run.find(id)
```

### Parameters

* `id` (int64): Required - Automation Run ID.

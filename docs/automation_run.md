# AutomationRun

## Example AutomationRun Object

```
{
  "automation_id": 1,
  "status": "success",
  "status_messages_url": "https://www.example.com/log_file.txt"
}
```

* `automation_id` (int64): ID of the associated Automation.
* `status` (string): The success status of the AutomationRun. One of `running`, `success`, `partial_failure`, or `failure`.
* `status_messages_url` (string): Link to status messages log file.


---

## List Automation Runs

```
files_sdk.automation_run.list({
  "user_id": 1,
  "per_page": 1,
  "automation_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `automation_id` (int64): Required - ID of the associated Automation.

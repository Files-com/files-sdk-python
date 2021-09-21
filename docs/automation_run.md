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
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `created_at` and `status`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `status`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `status`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `status`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `status`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `status`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `status`.
* `automation_id` (int64): Required - ID of the associated Automation.

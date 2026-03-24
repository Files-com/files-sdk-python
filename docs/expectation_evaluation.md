# ExpectationEvaluation

## Example ExpectationEvaluation Object

```
{
  "id": 1,
  "workspace_id": 1,
  "expectation_id": 1,
  "status": "open",
  "opened_via": "manual",
  "opened_at": "2000-01-01T01:00:00Z",
  "window_start_at": "2000-01-01T01:00:00Z",
  "window_end_at": "2000-01-01T01:00:00Z",
  "deadline_at": "2000-01-01T01:00:00Z",
  "late_acceptance_cutoff_at": "2000-01-01T01:00:00Z",
  "hard_close_at": "2000-01-01T01:00:00Z",
  "closed_at": "2000-01-01T01:00:00Z",
  "matched_files": [

  ],
  "missing_files": [

  ],
  "criteria_errors": [

  ],
  "summary": null,
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): ExpectationEvaluation ID
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.
* `expectation_id` (int64): Expectation ID.
* `status` (string): Evaluation status.
* `opened_via` (string): How the evaluation window was opened.
* `opened_at` (date-time): When the evaluation row was opened.
* `window_start_at` (date-time): Logical start of the candidate window.
* `window_end_at` (date-time): Actual candidate cutoff boundary for the window.
* `deadline_at` (date-time): Logical due boundary for schedule-driven windows.
* `late_acceptance_cutoff_at` (date-time): Logical cutoff for late acceptance, when present.
* `hard_close_at` (date-time): Hard stop after which the window may not remain open.
* `closed_at` (date-time): When the evaluation row was finalized.
* `matched_files` (array(object)): Captured evidence for files that matched the window.
* `missing_files` (array(object)): Captured evidence for required files that were missing.
* `criteria_errors` (array(object)): Captured criteria failures for the window.
* `summary` (object): Compact evaluator summary payload.
* `created_at` (date-time): Creation time.
* `updated_at` (date-time): Last update time.


---

## List Expectation Evaluations

```
files_sdk.expectation_evaluation.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `expectation_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `expectation_id` and `workspace_id`. Valid field combinations are `[ workspace_id, expectation_id ]`.


---

## Show Expectation Evaluation

```
files_sdk.expectation_evaluation.find(id)
```

### Parameters

* `id` (int64): Required - Expectation Evaluation ID.

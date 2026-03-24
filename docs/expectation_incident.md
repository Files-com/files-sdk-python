# ExpectationIncident

## Example ExpectationIncident Object

```
{
  "id": 1,
  "workspace_id": 1,
  "expectation_id": 1,
  "status": "open",
  "opened_at": "2000-01-01T01:00:00Z",
  "last_failed_at": "2000-01-01T01:00:00Z",
  "acknowledged_at": "2000-01-01T01:00:00Z",
  "snoozed_until": "2000-01-01T01:00:00Z",
  "resolved_at": "2000-01-01T01:00:00Z",
  "opened_by_evaluation_id": 1,
  "last_evaluation_id": 2,
  "resolved_by_evaluation_id": 3,
  "summary": null,
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Expectation Incident ID
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.
* `expectation_id` (int64): Expectation ID.
* `status` (string): Incident status.
* `opened_at` (date-time): When the incident was opened.
* `last_failed_at` (date-time): When the most recent failing evaluation contributing to the incident occurred.
* `acknowledged_at` (date-time): When the incident was acknowledged.
* `snoozed_until` (date-time): When the current snooze expires.
* `resolved_at` (date-time): When the incident was resolved.
* `opened_by_evaluation_id` (int64): Evaluation that first opened the incident.
* `last_evaluation_id` (int64): Most recent evaluation linked to the incident.
* `resolved_by_evaluation_id` (int64): Evaluation that resolved the incident.
* `summary` (object): Compact incident summary payload.
* `created_at` (date-time): Creation time.
* `updated_at` (date-time): Last update time.


---

## List Expectation Incidents

```
files_sdk.expectation_incident.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id`, `created_at` or `expectation_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `expectation_id` and `workspace_id`. Valid field combinations are `[ workspace_id, expectation_id ]`.


---

## Show Expectation Incident

```
files_sdk.expectation_incident.find(id)
```

### Parameters

* `id` (int64): Required - Expectation Incident ID.


---

## Resolve an expectation incident

```
files_sdk.expectation_incident.resolve(id)
```

### Parameters

* `id` (int64): Required - Expectation Incident ID.


---

## Snooze an expectation incident until a specified time

```
files_sdk.expectation_incident.snooze(id, {
  "snoozed_until": "snoozed_until"
})
```

### Parameters

* `id` (int64): Required - Expectation Incident ID.
* `snoozed_until` (string): Required - Time until which the incident should remain snoozed.


---

## Acknowledge an expectation incident

```
files_sdk.expectation_incident.acknowledge(id)
```

### Parameters

* `id` (int64): Required - Expectation Incident ID.


---

## Resolve an expectation incident

```
expectation_incident = files_sdk.expectation_incident.find(id)
expectation_incident.resolve()
```

### Parameters

* `id` (int64): Required - Expectation Incident ID.


---

## Snooze an expectation incident until a specified time

```
expectation_incident = files_sdk.expectation_incident.find(id)
expectation_incident.snooze({
  "snoozed_until": "snoozed_until"
})
```

### Parameters

* `id` (int64): Required - Expectation Incident ID.
* `snoozed_until` (string): Required - Time until which the incident should remain snoozed.


---

## Acknowledge an expectation incident

```
expectation_incident = files_sdk.expectation_incident.find(id)
expectation_incident.acknowledge()
```

### Parameters

* `id` (int64): Required - Expectation Incident ID.

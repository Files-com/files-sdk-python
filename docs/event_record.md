# EventRecord

## Example EventRecord Object

```
{
  "id": 1,
  "workspace_id": 1,
  "event_uuid": "example",
  "event_type": "example",
  "severity": "example",
  "source_type": "example",
  "source_id": 1,
  "occurred_at": "2000-01-01T01:00:00Z",
  "human_title": "example",
  "human_summary": "example",
  "human_fields": [
    "example"
  ],
  "actor": "example",
  "resources": [
    "example"
  ],
  "payload": "example",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Event Record ID
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `event_uuid` (string): Stable event UUID.
* `event_type` (string): Versioned event type string.
* `severity` (string): Event severity.
* `source_type` (string): Source record type.
* `source_id` (int64): Source record ID.
* `occurred_at` (date-time): Event occurrence date/time.
* `human_title` (string): Human-readable event title.
* `human_summary` (string): Human-readable event summary.
* `human_fields` (array(object)): Human-readable event detail fields.
* `actor` (object): Actor associated with the event.
* `resources` (array(object)): Resources associated with the event.
* `payload` (object): Event payload.
* `created_at` (date-time): Event Record create date/time.


---

## List Event Records

```
files_sdk.event_record.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `event_type`, `created_at` or `workspace_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `event_type` or `workspace_id`. Valid field combinations are `[ event_type, created_at ]`, `[ workspace_id, created_at ]`, `[ workspace_id, event_type ]` or `[ workspace_id, event_type, created_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `event_type`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.


---

## Show Event Record

```
files_sdk.event_record.find(id)
```

### Parameters

* `id` (int64): Required - Event Record ID.


---

## Create an export CSV of Event Record resources

```
files_sdk.event_record.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `event_type`, `created_at` or `workspace_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `event_type` or `workspace_id`. Valid field combinations are `[ event_type, created_at ]`, `[ workspace_id, created_at ]`, `[ workspace_id, event_type ]` or `[ workspace_id, event_type, created_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `event_type`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.

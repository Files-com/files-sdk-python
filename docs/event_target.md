# EventTarget

## Example EventTarget Object

The API sends each `EventTarget` record as JSON, such as:

```json
{
  "id": 1,
  "name": "example",
  "target_type": "webhook",
  "workspace_id": 1,
  "apply_to_all_workspaces": true,
  "enabled": true,
  "config": {
    "url": "https://example.com/files-events",
    "headers": {
      "X-Example": "value"
    },
    "use_dedicated_ips": false
  },
  "delivery_policy": {
    "max_attempts": 3,
    "retry_delay_minutes": [
      1,
      10
    ]
  },
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Event Target ID
* `name` (string): Event Target name.
* `target_type` (string): Event Target type.
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace target can receive events from all workspaces.
* `enabled` (boolean): Whether this Event Target can receive events.
* `config` (object): Event Target configuration. Fields depend on target_type.
* `delivery_policy` (object): Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
* `created_at` (date-time): Event Target create date/time.
* `updated_at` (date-time): Event Target update date/time.

The functions below use the module's settings. Each is also a method of a client's
`client.event_target` resource, such as
`client.event_target.list(...)`,
which uses that client's configuration instead.


---

## List Event Targets

```python
files_sdk.event_target.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `name`, `enabled` or `workspace_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `enabled`, `target_type` or `workspace_id`. Valid field combinations are `[ enabled, target_type ]`, `[ workspace_id, enabled ]` or `[ workspace_id, enabled, target_type ]`.


---

## Show Event Target

```python
files_sdk.event_target.find(id)
```

### Parameters

* `id` (int64): Required - Event Target ID.


---

## Create Event Target

```python
files_sdk.event_target.create({
  "name": "example",
  "workspace_id": 1,
  "apply_to_all_workspaces": True,
  "enabled": True,
  "config": {"url": "https://example.com/files-events", "headers": {"X-Example": "value"}, "use_dedicated_ips": False},
  "delivery_policy": {"max_attempts": 3, "retry_delay_minutes": [1, 10]},
  "target_type": "webhook"
})
```

### Parameters

* `name` (string): Required - Event Target name.
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace target can receive events from all workspaces.
* `enabled` (boolean): Whether this Event Target can receive events.
* `config` (object): Required - Event Target configuration. Fields depend on target_type.
* `delivery_policy` (object): Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.
* `target_type` (string): Required - Event Target type.


---

## Update Event Target

```python
files_sdk.event_target.update(id, {
  "name": "example",
  "workspace_id": 1,
  "apply_to_all_workspaces": True,
  "enabled": True,
  "config": {"url": "https://example.com/files-events", "headers": {"X-Example": "value"}, "use_dedicated_ips": False},
  "delivery_policy": {"max_attempts": 3, "retry_delay_minutes": [1, 10]}
})
```

### Parameters

* `id` (int64): Required - Event Target ID.
* `name` (string): Event Target name.
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace target can receive events from all workspaces.
* `enabled` (boolean): Whether this Event Target can receive events.
* `config` (object): Event Target configuration. Fields depend on target_type.
* `delivery_policy` (object): Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.


---

## Delete Event Target

```python
files_sdk.event_target.delete(id)
```

### Parameters

* `id` (int64): Required - Event Target ID.


---

## Update Event Target

```python
event_target = files_sdk.event_target.find(id)
event_target.update({
  "name": "example",
  "workspace_id": 1,
  "apply_to_all_workspaces": True,
  "enabled": True,
  "config": {"url": "https://example.com/files-events", "headers": {"X-Example": "value"}, "use_dedicated_ips": False},
  "delivery_policy": {"max_attempts": 3, "retry_delay_minutes": [1, 10]}
})
```

### Parameters

* `id` (int64): Required - Event Target ID.
* `name` (string): Event Target name.
* `workspace_id` (int64): Workspace ID. 0 means the default workspace or site-wide.
* `apply_to_all_workspaces` (boolean): If true, this default-workspace target can receive events from all workspaces.
* `enabled` (boolean): Whether this Event Target can receive events.
* `config` (object): Event Target configuration. Fields depend on target_type.
* `delivery_policy` (object): Event Target delivery policy. Email and folder targets support batch_interval in seconds, between 600 and 86400. Slack and Teams support delivery_mode (immediate or subfolder_summary), summary_path (empty string means root), and summary_delay (15–300 seconds, default 60). The summary applies to matching file activity under summary_path; other matching events retain immediate delivery.


---

## Delete Event Target

```python
event_target = files_sdk.event_target.find(id)
event_target.delete()
```

### Parameters

* `id` (int64): Required - Event Target ID.

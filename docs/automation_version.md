# AutomationVersion

## Example AutomationVersion Object

The API sends each `AutomationVersion` record as JSON, such as:

```json
{
  "id": 1,
  "automation_id": 1,
  "workspace_id": 1,
  "version": 1,
  "created_at": "2000-01-01T01:00:00Z",
  "user_id": 1,
  "username": "example",
  "api_key_id": 1,
  "definition": {
    "schema_version": 1,
    "nodes": [
      {
        "id": "trigger",
        "type": "trigger_manual"
      },
      {
        "id": "create_reports",
        "type": "create_folder",
        "config": {
          "destinations": [
            "reports/"
          ]
        }
      }
    ],
    "edges": [
      {
        "from": "trigger",
        "to": "create_reports"
      }
    ]
  }
}
```

* `id` (int64): Automation revision ID.
* `automation_id` (int64): ID of the Automation that owns this revision.
* `workspace_id` (int64): Workspace that owns the Automation. Zero is the Default Workspace.
* `version` (int64): Revision number within the Automation.
* `created_at` (date-time): Time the revision was saved.
* `user_id` (int64): ID of the user who saved the revision, when available.
* `username` (string): Username recorded when the revision was saved, when available.
* `api_key_id` (int64): ID of the API key used to save the revision, when available.
* `definition` (object): Saved Automation v2 graph definition. Included when retrieving a single revision.

The functions below use the module's settings. Each is also a method of a client's
`client.automation_version` resource, such as
`client.automation_version.list(...)`,
which uses that client's configuration instead.


---

## List Automation Versions

```python
files_sdk.automation_version.list({
  "automation_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
* `automation_id` (int64): Required - ID of the Automation that owns this revision.


---

## Show Automation Version

```python
files_sdk.automation_version.find(id)
```

### Parameters

* `id` (int64): Required - Automation Version ID.


---

## Restore an Automation v2 definition as a new current version

```python
files_sdk.automation_version.restore(id)
```

### Parameters

* `id` (int64): Required - Automation Version ID.


---

## Restore an Automation v2 definition as a new current version

```python
automation_version = files_sdk.automation_version.find(id)
automation_version.restore()
```

### Parameters

* `id` (int64): Required - Automation Version ID.

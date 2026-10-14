# KeyLifecycleRule

## Example KeyLifecycleRule Object

The API sends each `KeyLifecycleRule` record as JSON, such as:

```json
{
  "id": 1,
  "key_type": "gpg",
  "inactivity_days": 12,
  "expiration_days": 365,
  "apply_to_all_workspaces": true,
  "name": "inactive gpg keys",
  "workspace_id": 12
}
```

* `id` (int64): Key Lifecycle Rule ID
* `key_type` (string): Key type for which the rule will apply (gpg, ssh, or api).
* `inactivity_days` (int64): Number of days of inactivity before the rule applies.
* `expiration_days` (int64): Number of days after creation before an SSH key expires. Applies only to SSH keys.
* `apply_to_all_workspaces` (boolean): If true, a default-workspace rule also applies to keys in all workspaces.
* `name` (string): Key Lifecycle Rule name
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.

The functions below use the module's settings. Each is also a method of a client's
`client.key_lifecycle_rule` resource, such as
`client.key_lifecycle_rule.list(...)`,
which uses that client's configuration instead.


---

## List Key Lifecycle Rules

```python
files_sdk.key_lifecycle_rule.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `workspace_id` and `key_type`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `key_type` and `workspace_id`. Valid field combinations are `[ workspace_id, key_type ]`.


---

## Show Key Lifecycle Rule

```python
files_sdk.key_lifecycle_rule.find(id)
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.


---

## Create Key Lifecycle Rule

```python
files_sdk.key_lifecycle_rule.create({
  "apply_to_all_workspaces": True,
  "expiration_days": 365,
  "key_type": "gpg",
  "inactivity_days": 12,
  "name": "inactive gpg keys",
  "workspace_id": 12
})
```

### Parameters

* `apply_to_all_workspaces` (boolean): If true, a default-workspace rule also applies to keys in all workspaces.
* `expiration_days` (int64): Number of days after creation before an SSH key expires. Applies only to SSH keys.
* `key_type` (string): Key type for which the rule will apply (gpg, ssh, or api).
* `inactivity_days` (int64): Number of days of inactivity before the rule applies.
* `name` (string): Key Lifecycle Rule name
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Update Key Lifecycle Rule

```python
files_sdk.key_lifecycle_rule.update(id, {
  "apply_to_all_workspaces": True,
  "expiration_days": 365,
  "key_type": "gpg",
  "inactivity_days": 12,
  "name": "inactive gpg keys",
  "workspace_id": 12
})
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.
* `apply_to_all_workspaces` (boolean): If true, a default-workspace rule also applies to keys in all workspaces.
* `expiration_days` (int64): Number of days after creation before an SSH key expires. Applies only to SSH keys.
* `key_type` (string): Key type for which the rule will apply (gpg, ssh, or api).
* `inactivity_days` (int64): Number of days of inactivity before the rule applies.
* `name` (string): Key Lifecycle Rule name
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Delete Key Lifecycle Rule

```python
files_sdk.key_lifecycle_rule.delete(id)
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.


---

## Update Key Lifecycle Rule

```python
key_lifecycle_rule = files_sdk.key_lifecycle_rule.find(id)
key_lifecycle_rule.update({
  "apply_to_all_workspaces": True,
  "expiration_days": 365,
  "key_type": "gpg",
  "inactivity_days": 12,
  "name": "inactive gpg keys",
  "workspace_id": 12
})
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.
* `apply_to_all_workspaces` (boolean): If true, a default-workspace rule also applies to keys in all workspaces.
* `expiration_days` (int64): Number of days after creation before an SSH key expires. Applies only to SSH keys.
* `key_type` (string): Key type for which the rule will apply (gpg, ssh, or api).
* `inactivity_days` (int64): Number of days of inactivity before the rule applies.
* `name` (string): Key Lifecycle Rule name
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Delete Key Lifecycle Rule

```python
key_lifecycle_rule = files_sdk.key_lifecycle_rule.find(id)
key_lifecycle_rule.delete()
```

### Parameters

* `id` (int64): Required - Key Lifecycle Rule ID.

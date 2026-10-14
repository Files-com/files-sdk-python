# Snapshot

## Example Snapshot Object

The API sends each `Snapshot` record as JSON, such as:

```json
{
  "id": 1,
  "expires_at": "2000-01-01T01:00:00Z",
  "finalized_at": "2000-01-01T01:00:00Z",
  "name": "My Snapshot",
  "user_id": 1,
  "bundle_id": 1,
  "workspace_id": 1
}
```

* `id` (int64): The snapshot's unique ID.
* `expires_at` (date-time): When the snapshot expires.
* `finalized_at` (date-time): When the snapshot was finalized.
* `name` (string): A name for the snapshot.
* `user_id` (int64): The user that created this snapshot, if applicable.
* `bundle_id` (int64): The bundle using this snapshot, if applicable.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.
* `paths` (array(string)): An array of paths to add to the snapshot.

The functions below use the module's settings. Each is also a method of a client's
`client.snapshot` resource, such as
`client.snapshot.list(...)`,
which uses that client's configuration instead.


---

## List Snapshots

```python
files_sdk.snapshot.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Show Snapshot

```python
files_sdk.snapshot.find(id)
```

### Parameters

* `id` (int64): Required - Snapshot ID.


---

## Create Snapshot

```python
files_sdk.snapshot.create({
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "My Snapshot",
  "workspace_id": 0
})
```

### Parameters

* `expires_at` (string): When the snapshot expires.
* `name` (string): A name for the snapshot.
* `paths` (array(string)): An array of paths to add to the snapshot.
* `workspace_id` (int64): Workspace ID. `0` means the default workspace.


---

## Finalize Snapshot

```python
files_sdk.snapshot.finalize(id)
```

### Parameters

* `id` (int64): Required - Snapshot ID.


---

## Update Snapshot

```python
files_sdk.snapshot.update(id, {
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "My Snapshot"
})
```

### Parameters

* `id` (int64): Required - Snapshot ID.
* `expires_at` (string): When the snapshot expires.
* `name` (string): A name for the snapshot.
* `paths` (array(string)): An array of paths to add to the snapshot.


---

## Delete Snapshot

```python
files_sdk.snapshot.delete(id)
```

### Parameters

* `id` (int64): Required - Snapshot ID.


---

## Finalize Snapshot

```python
snapshot = files_sdk.snapshot.find(id)
snapshot.finalize()
```

### Parameters

* `id` (int64): Required - Snapshot ID.


---

## Update Snapshot

```python
snapshot = files_sdk.snapshot.find(id)
snapshot.update({
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "My Snapshot"
})
```

### Parameters

* `id` (int64): Required - Snapshot ID.
* `expires_at` (string): When the snapshot expires.
* `name` (string): A name for the snapshot.
* `paths` (array(string)): An array of paths to add to the snapshot.


---

## Delete Snapshot

```python
snapshot = files_sdk.snapshot.find(id)
snapshot.delete()
```

### Parameters

* `id` (int64): Required - Snapshot ID.

# Snapshot

## Example Snapshot Object

```
{
  "id": 1,
  "expires_at": "2000-01-01T01:00:00Z",
  "finalized_at": "2000-01-01T01:00:00Z",
  "name": "My Snapshot",
  "user_id": 1,
  "bundle_id": 1
}
```

* `id` (int64): The snapshot's unique ID.
* `expires_at` (date-time): When the snapshot expires.
* `finalized_at` (date-time): When the snapshot was finalized.
* `name` (string): A name for the snapshot.
* `user_id` (int64): The user that created this snapshot, if applicable.
* `bundle_id` (int64): The bundle using this snapshot, if applicable.
* `paths` (array(string)): An array of paths to add to the snapshot.


---

## List Snapshots

```
files_sdk.snapshot.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 


---

## Show Snapshot

```
files_sdk.snapshot.find(id)
```

### Parameters

* `id` (int64): Required - Snapshot ID.


---

## Create Snapshot

```
files_sdk.snapshot.create({
  "expires_at": "2000-01-01T01:00:00Z",
  "name": "My Snapshot"
})
```

### Parameters

* `expires_at` (string): When the snapshot expires.
* `name` (string): A name for the snapshot.
* `paths` (array(string)): An array of paths to add to the snapshot.


---

## Finalize Snapshot

```
files_sdk.snapshot.finalize(id)
```

### Parameters

* `id` (int64): Required - Snapshot ID.


---

## Update Snapshot

```
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

```
files_sdk.snapshot.delete(id)
```

### Parameters

* `id` (int64): Required - Snapshot ID.


---

## Finalize Snapshot

```
snapshot = files_sdk.snapshot.find(id)
snapshot.finalize()
```

### Parameters

* `id` (int64): Required - Snapshot ID.


---

## Update Snapshot

```
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

```
snapshot = files_sdk.snapshot.find(id)
snapshot.delete()
```

### Parameters

* `id` (int64): Required - Snapshot ID.

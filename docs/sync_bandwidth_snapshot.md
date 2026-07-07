# SyncBandwidthSnapshot

## Example SyncBandwidthSnapshot Object

```
{
  "id": 1,
  "site_id": 123,
  "sync_bytes_received": "1.0",
  "sync_bytes_sent": "1.0",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): sync bandwidth snapshot ID
* `site_id` (int64): Site ID
* `sync_bytes_received` (decimal): bytes received
* `sync_bytes_sent` (decimal): bytes sent
* `created_at` (date-time): sync bandwidth snapshot created at date/time
* `remote_server_id` (int64): ID for the remote server consuming sync bandwidth


---

## Create Sync Bandwidth Snapshot

```
files_sdk.sync_bandwidth_snapshot.create({
  "remote_server_id": 1,
  "sync_bytes_sent": 1,
  "sync_bytes_received": 1
})
```

### Parameters

* `remote_server_id` (int64): Required - ID for the remote server consuming sync bandwidth
* `sync_bytes_sent` (int64): Required - Sync bytes sent
* `sync_bytes_received` (int64): Required - Sync bytes received


---

## Create Sync Bandwidth Snapshots

```
files_sdk.sync_bandwidth_snapshot.create_batch()
```

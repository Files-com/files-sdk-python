# RemoteMountBackend

## Example RemoteMountBackend Object

```
{
  "canary_file_path": "backend1.txt",
  "enabled": True,
  "fall": 1,
  "health_check_enabled": True,
  "health_check_results": [
    {
      "timestamp": "2025-09-19T12:32:52+00:00",
      "status": "healthy",
      "canary_timestamp": "2025-09-19T12:32:52+00:00"
    },
    {
      "status": "failed",
      "reason": "Unable to connect",
      "timestamp": "2025-09-19T12:32:52+00:00"
    }
  ],
  "health_check_type": "active",
  "id": 1,
  "interval": 60,
  "min_free_cpu": 1.0,
  "min_free_mem": 1.0,
  "priority": 1,
  "remote_path": "/path/on/remote",
  "remote_server_id": 1,
  "remote_server_mount_id": 1,
  "rise": 1,
  "status": "healthy",
  "undergoing_maintenance": True
}
```

* `canary_file_path` (string): Path to the canary file used for health checks.
* `enabled` (boolean): True if this backend is enabled.
* `fall` (int64): Number of consecutive failures before considering the backend unhealthy.
* `health_check_enabled` (boolean): True if health checks are enabled for this backend.
* `health_check_results` (array(object)): Array of recent health check results.
* `health_check_type` (string): Type of health check to perform.
* `id` (int64): Unique identifier for this backend.
* `interval` (int64): Interval in seconds between health checks.
* `min_free_cpu` (double): Minimum free CPU percentage required for this backend to be considered healthy.
* `min_free_mem` (double): Minimum free memory percentage required for this backend to be considered healthy.
* `priority` (int64): Priority of this backend.
* `remote_path` (string): Path on the remote server to treat as the root of this mount.
* `remote_server_id` (int64): The remote server that this backend is associated with.
* `remote_server_mount_id` (int64): The mount ID of the Remote Server Mount that this backend is associated with.
* `rise` (int64): Number of consecutive successes before considering the backend healthy.
* `status` (string): Status of this backend.
* `undergoing_maintenance` (boolean): True if this backend is undergoing maintenance.


---

## List Remote Mount Backends

```
files_sdk.remote_mount_backend.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `remote_server_mount_id`.


---

## Show Remote Mount Backend

```
files_sdk.remote_mount_backend.find(id)
```

### Parameters

* `id` (int64): Required - Remote Mount Backend ID.


---

## Create Remote Mount Backend

```
files_sdk.remote_mount_backend.create({
  "enabled": True,
  "fall": 1,
  "health_check_enabled": True,
  "health_check_type": "active",
  "interval": 60,
  "min_free_cpu": 1.0,
  "min_free_mem": 1.0,
  "priority": 1,
  "remote_path": "/path/on/remote",
  "rise": 1,
  "canary_file_path": "backend1.txt",
  "remote_server_mount_id": 1,
  "remote_server_id": 1
})
```

### Parameters

* `enabled` (boolean): True if this backend is enabled.
* `fall` (int64): Number of consecutive failures before considering the backend unhealthy.
* `health_check_enabled` (boolean): True if health checks are enabled for this backend.
* `health_check_type` (string): Type of health check to perform.
* `interval` (int64): Interval in seconds between health checks.
* `min_free_cpu` (double): Minimum free CPU percentage required for this backend to be considered healthy.
* `min_free_mem` (double): Minimum free memory percentage required for this backend to be considered healthy.
* `priority` (int64): Priority of this backend.
* `remote_path` (string): Path on the remote server to treat as the root of this mount.
* `rise` (int64): Number of consecutive successes before considering the backend healthy.
* `canary_file_path` (string): Required - Path to the canary file used for health checks.
* `remote_server_mount_id` (int64): Required - The mount ID of the Remote Server Mount that this backend is associated with.
* `remote_server_id` (int64): Required - The remote server that this backend is associated with.


---

## Reset backend status to healthy

```
files_sdk.remote_mount_backend.reset_status(id)
```

### Parameters

* `id` (int64): Required - Remote Mount Backend ID.


---

## Update Remote Mount Backend

```
files_sdk.remote_mount_backend.update(id, {
  "enabled": True,
  "fall": 1,
  "health_check_enabled": True,
  "health_check_type": "active",
  "interval": 60,
  "min_free_cpu": 1.0,
  "min_free_mem": 1.0,
  "priority": 1,
  "remote_path": "/path/on/remote",
  "rise": 1,
  "canary_file_path": "backend1.txt",
  "remote_server_id": 1
})
```

### Parameters

* `id` (int64): Required - Remote Mount Backend ID.
* `enabled` (boolean): True if this backend is enabled.
* `fall` (int64): Number of consecutive failures before considering the backend unhealthy.
* `health_check_enabled` (boolean): True if health checks are enabled for this backend.
* `health_check_type` (string): Type of health check to perform.
* `interval` (int64): Interval in seconds between health checks.
* `min_free_cpu` (double): Minimum free CPU percentage required for this backend to be considered healthy.
* `min_free_mem` (double): Minimum free memory percentage required for this backend to be considered healthy.
* `priority` (int64): Priority of this backend.
* `remote_path` (string): Path on the remote server to treat as the root of this mount.
* `rise` (int64): Number of consecutive successes before considering the backend healthy.
* `canary_file_path` (string): Path to the canary file used for health checks.
* `remote_server_id` (int64): The remote server that this backend is associated with.


---

## Delete Remote Mount Backend

```
files_sdk.remote_mount_backend.delete(id)
```

### Parameters

* `id` (int64): Required - Remote Mount Backend ID.


---

## Reset backend status to healthy

```
remote_mount_backend = files_sdk.remote_mount_backend.find(id)
remote_mount_backend.reset_status()
```

### Parameters

* `id` (int64): Required - Remote Mount Backend ID.


---

## Update Remote Mount Backend

```
remote_mount_backend = files_sdk.remote_mount_backend.find(id)
remote_mount_backend.update({
  "enabled": True,
  "fall": 1,
  "health_check_enabled": True,
  "health_check_type": "active",
  "interval": 60,
  "min_free_cpu": 1.0,
  "min_free_mem": 1.0,
  "priority": 1,
  "remote_path": "/path/on/remote",
  "rise": 1,
  "canary_file_path": "backend1.txt",
  "remote_server_id": 1
})
```

### Parameters

* `id` (int64): Required - Remote Mount Backend ID.
* `enabled` (boolean): True if this backend is enabled.
* `fall` (int64): Number of consecutive failures before considering the backend unhealthy.
* `health_check_enabled` (boolean): True if health checks are enabled for this backend.
* `health_check_type` (string): Type of health check to perform.
* `interval` (int64): Interval in seconds between health checks.
* `min_free_cpu` (double): Minimum free CPU percentage required for this backend to be considered healthy.
* `min_free_mem` (double): Minimum free memory percentage required for this backend to be considered healthy.
* `priority` (int64): Priority of this backend.
* `remote_path` (string): Path on the remote server to treat as the root of this mount.
* `rise` (int64): Number of consecutive successes before considering the backend healthy.
* `canary_file_path` (string): Path to the canary file used for health checks.
* `remote_server_id` (int64): The remote server that this backend is associated with.


---

## Delete Remote Mount Backend

```
remote_mount_backend = files_sdk.remote_mount_backend.find(id)
remote_mount_backend.delete()
```

### Parameters

* `id` (int64): Required - Remote Mount Backend ID.

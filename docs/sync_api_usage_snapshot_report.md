# SyncApiUsageSnapshotReport

## Example SyncApiUsageSnapshotReport Object

```
{
  "start_time": "2000-01-01T01:00:00Z",
  "end_time": "2000-01-01T01:00:00Z",
  "uuid": "example",
  "auth_cache_hits": 1,
  "auth_cache_misses": 1,
  "auth_api_requests_for_sftp": 1,
  "auth_api_requests_for_ftp": 1,
  "auth_api_requests_for_dav": 1,
  "auth_api_requests_for_desktop": 1,
  "auth_api_requests_for_restapi": 1,
  "number_of_sync_api_usage_snapshots": 1,
  "sync_api_usage_snapshots": [

  ]
}
```

* `start_time` (date-time): start time of statistics collection
* `end_time` (date-time): end time of statistics collection
* `uuid` (string): Unique ID for this entry
* `auth_cache_hits` (int64): Numbers of hits of the authentication cache
* `auth_cache_misses` (int64): Numbers of misses of the authentication cache
* `auth_api_requests_for_sftp` (int64): A count of api authentications requests for SFTP
* `auth_api_requests_for_ftp` (int64): A count of api authentications requests for FTP
* `auth_api_requests_for_dav` (int64): A count of api authentications requests for DAV
* `auth_api_requests_for_desktop` (int64): A count of api authentications requests for Desktop
* `auth_api_requests_for_restapi` (int64): A count of api authentications requests for Restapi
* `number_of_sync_api_usage_snapshots` (int64): A count of the number of api usage logs
* `sync_api_usage_snapshots` (array(object)): A list of all the api usage logs


---

## Create Sync API Usage Snapshot Report

```
files_sdk.sync_api_usage_snapshot_report.create({
  "start_time": "2000-01-01T01:00:00Z",
  "end_time": "2000-01-01T01:00:00Z",
  "uuid": "example",
  "auth_cache_hits": 1,
  "auth_cache_misses": 1,
  "auth_api_requests_for_sftp": 1,
  "auth_api_requests_for_ftp": 1,
  "auth_api_requests_for_dav": 1,
  "auth_api_requests_for_desktop": 1,
  "auth_api_requests_for_restapi": 1,
  "number_of_sync_api_usage_snapshots": 1
})
```

### Parameters

* `start_time` (string): start time of statistics collection
* `end_time` (string): end time of statistics collection
* `uuid` (string): Unique ID for this entry
* `auth_cache_hits` (int64): Numbers of hits of the authentication cache
* `auth_cache_misses` (int64): Numbers of misses of the authentication cache
* `auth_api_requests_for_sftp` (int64): A count of api authentications requests for SFTP
* `auth_api_requests_for_ftp` (int64): A count of api authentications requests for FTP
* `auth_api_requests_for_dav` (int64): A count of api authentications requests for DAV
* `auth_api_requests_for_desktop` (int64): A count of api authentications requests for Desktop
* `auth_api_requests_for_restapi` (int64): A count of api authentications requests for Restapi
* `number_of_sync_api_usage_snapshots` (int64): A count of the number of api usage logs
* `sync_api_usage_snapshots` (array(object)): 

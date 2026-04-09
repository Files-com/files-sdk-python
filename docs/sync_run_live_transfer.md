# SyncRunLiveTransfer

## Example SyncRunLiveTransfer Object

```
{
  "path": "example",
  "status": "example",
  "bytes_copied": 1,
  "bytes_total": 1,
  "percentage": 1.0,
  "eta": "example",
  "started_at": "example"
}
```

* `path` (string): The file path being transferred. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `status` (string): Status of this individual transfer
* `bytes_copied` (int64): Bytes transferred so far
* `bytes_total` (int64): Total bytes of the file being transferred
* `percentage` (double): Transfer progress from 0.0 to 1.0
* `eta` (string): Estimated time remaining (human-readable)
* `started_at` (string): When this individual transfer started

# FileMigration

## Example FileMigration Object

The API sends each `FileMigration` record as JSON, such as:

```json
{
  "id": 1,
  "path": "MyFolder",
  "dest_path": "MyFolder",
  "failure_message": "example",
  "files_moved": 1,
  "files_total": 1,
  "operation": "move",
  "region": "USA",
  "status": "complete",
  "log_url": "https://www.example.com/log_file"
}
```

* `id` (int64): File migration ID
* `path` (string): Source path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `dest_path` (string): Destination path
* `failure_message` (string): Reason for the failure, if applicable.
* `files_moved` (int64): Number of files processed
* `files_total` (int64): 
* `operation` (string): The type of operation
* `region` (string): Region
* `status` (string): Status
* `log_url` (string): Link to download the log file for this migration.

The functions below use the module's settings. Each is also a method of a client's
`client.file_migration` resource, such as
`client.file_migration.find(...)`,
which uses that client's configuration instead.


---

## Show File Migration

```python
files_sdk.file_migration.find(id)
```

### Parameters

* `id` (int64): Required - File Migration ID.

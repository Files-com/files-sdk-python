# FileMigration

## Example FileMigration Object

```
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


---

## List in-progress file migrations. Returns the 10 most recently active migrations, after narrowing the list to remove overlapping operations

```
files_sdk.file_migration.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).


---

## Show File Migration

```
files_sdk.file_migration.find(id)
```

### Parameters

* `id` (int64): Required - File Migration ID.


---

## List in-progress file migrations. Returns the 10 most recently active migrations, after narrowing the list to remove overlapping operations

```
files_sdk.file_migration.create_export({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.

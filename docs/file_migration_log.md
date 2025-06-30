# FileMigrationLog

## Example FileMigrationLog Object

```
{
  "timestamp": "2000-01-01T01:00:00Z",
  "file_migration_id": 1,
  "dest_path": "example",
  "error_type": "example",
  "message": "example",
  "operation": "example",
  "path": "example",
  "status": "example",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `timestamp` (date-time): Start Time of Action. Deprecrated: Use created_at.
* `file_migration_id` (int64): File Migration ID
* `dest_path` (string): Destination path, for moves and copies
* `error_type` (string): Error type, if applicable
* `message` (string): Message
* `operation` (string): Operation type
* `path` (string): File path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `status` (string): Status
* `created_at` (date-time): Start Time of Action


---

## List File Migration Logs

```
files_sdk.file_migration_log.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `file_migration_id`, `operation`, `status`, `type` or `created_at`. Valid field combinations are `[ file_migration_id ]`, `[ operation ]`, `[ status ]`, `[ type ]`, `[ created_at ]`, `[ file_migration_id, operation ]`, `[ file_migration_id, status ]`, `[ file_migration_id, type ]`, `[ file_migration_id, created_at ]`, `[ operation, status ]`, `[ operation, type ]`, `[ operation, created_at ]`, `[ status, type ]`, `[ status, created_at ]`, `[ type, created_at ]`, `[ file_migration_id, operation, status ]`, `[ file_migration_id, operation, type ]`, `[ file_migration_id, operation, created_at ]`, `[ file_migration_id, status, type ]`, `[ file_migration_id, status, created_at ]`, `[ file_migration_id, type, created_at ]`, `[ operation, status, type ]`, `[ operation, status, created_at ]`, `[ operation, type, created_at ]`, `[ status, type, created_at ]`, `[ file_migration_id, operation, status, type ]`, `[ file_migration_id, operation, status, created_at ]`, `[ file_migration_id, operation, type, created_at ]`, `[ file_migration_id, status, type, created_at ]`, `[ operation, status, type, created_at ]` or `[ file_migration_id, operation, status, type, created_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ file_migration_id ]`, `[ operation ]`, `[ status ]`, `[ type ]`, `[ created_at ]`, `[ file_migration_id, operation ]`, `[ file_migration_id, status ]`, `[ file_migration_id, type ]`, `[ file_migration_id, created_at ]`, `[ operation, status ]`, `[ operation, type ]`, `[ operation, created_at ]`, `[ status, type ]`, `[ status, created_at ]`, `[ type, created_at ]`, `[ file_migration_id, operation, status ]`, `[ file_migration_id, operation, type ]`, `[ file_migration_id, operation, created_at ]`, `[ file_migration_id, status, type ]`, `[ file_migration_id, status, created_at ]`, `[ file_migration_id, type, created_at ]`, `[ operation, status, type ]`, `[ operation, status, created_at ]`, `[ operation, type, created_at ]`, `[ status, type, created_at ]`, `[ file_migration_id, operation, status, type ]`, `[ file_migration_id, operation, status, created_at ]`, `[ file_migration_id, operation, type, created_at ]`, `[ file_migration_id, status, type, created_at ]`, `[ operation, status, type, created_at ]` or `[ file_migration_id, operation, status, type, created_at ]`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ file_migration_id ]`, `[ operation ]`, `[ status ]`, `[ type ]`, `[ created_at ]`, `[ file_migration_id, operation ]`, `[ file_migration_id, status ]`, `[ file_migration_id, type ]`, `[ file_migration_id, created_at ]`, `[ operation, status ]`, `[ operation, type ]`, `[ operation, created_at ]`, `[ status, type ]`, `[ status, created_at ]`, `[ type, created_at ]`, `[ file_migration_id, operation, status ]`, `[ file_migration_id, operation, type ]`, `[ file_migration_id, operation, created_at ]`, `[ file_migration_id, status, type ]`, `[ file_migration_id, status, created_at ]`, `[ file_migration_id, type, created_at ]`, `[ operation, status, type ]`, `[ operation, status, created_at ]`, `[ operation, type, created_at ]`, `[ status, type, created_at ]`, `[ file_migration_id, operation, status, type ]`, `[ file_migration_id, operation, status, created_at ]`, `[ file_migration_id, operation, type, created_at ]`, `[ file_migration_id, status, type, created_at ]`, `[ operation, status, type, created_at ]` or `[ file_migration_id, operation, status, type, created_at ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `operation` and `status`. Valid field combinations are `[ file_migration_id ]`, `[ operation ]`, `[ status ]`, `[ type ]`, `[ created_at ]`, `[ file_migration_id, operation ]`, `[ file_migration_id, status ]`, `[ file_migration_id, type ]`, `[ file_migration_id, created_at ]`, `[ operation, status ]`, `[ operation, type ]`, `[ operation, created_at ]`, `[ status, type ]`, `[ status, created_at ]`, `[ type, created_at ]`, `[ file_migration_id, operation, status ]`, `[ file_migration_id, operation, type ]`, `[ file_migration_id, operation, created_at ]`, `[ file_migration_id, status, type ]`, `[ file_migration_id, status, created_at ]`, `[ file_migration_id, type, created_at ]`, `[ operation, status, type ]`, `[ operation, status, created_at ]`, `[ operation, type, created_at ]`, `[ status, type, created_at ]`, `[ file_migration_id, operation, status, type ]`, `[ file_migration_id, operation, status, created_at ]`, `[ file_migration_id, operation, type, created_at ]`, `[ file_migration_id, status, type, created_at ]`, `[ operation, status, type, created_at ]` or `[ file_migration_id, operation, status, type, created_at ]`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ file_migration_id ]`, `[ operation ]`, `[ status ]`, `[ type ]`, `[ created_at ]`, `[ file_migration_id, operation ]`, `[ file_migration_id, status ]`, `[ file_migration_id, type ]`, `[ file_migration_id, created_at ]`, `[ operation, status ]`, `[ operation, type ]`, `[ operation, created_at ]`, `[ status, type ]`, `[ status, created_at ]`, `[ type, created_at ]`, `[ file_migration_id, operation, status ]`, `[ file_migration_id, operation, type ]`, `[ file_migration_id, operation, created_at ]`, `[ file_migration_id, status, type ]`, `[ file_migration_id, status, created_at ]`, `[ file_migration_id, type, created_at ]`, `[ operation, status, type ]`, `[ operation, status, created_at ]`, `[ operation, type, created_at ]`, `[ status, type, created_at ]`, `[ file_migration_id, operation, status, type ]`, `[ file_migration_id, operation, status, created_at ]`, `[ file_migration_id, operation, type, created_at ]`, `[ file_migration_id, status, type, created_at ]`, `[ operation, status, type, created_at ]` or `[ file_migration_id, operation, status, type, created_at ]`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ file_migration_id ]`, `[ operation ]`, `[ status ]`, `[ type ]`, `[ created_at ]`, `[ file_migration_id, operation ]`, `[ file_migration_id, status ]`, `[ file_migration_id, type ]`, `[ file_migration_id, created_at ]`, `[ operation, status ]`, `[ operation, type ]`, `[ operation, created_at ]`, `[ status, type ]`, `[ status, created_at ]`, `[ type, created_at ]`, `[ file_migration_id, operation, status ]`, `[ file_migration_id, operation, type ]`, `[ file_migration_id, operation, created_at ]`, `[ file_migration_id, status, type ]`, `[ file_migration_id, status, created_at ]`, `[ file_migration_id, type, created_at ]`, `[ operation, status, type ]`, `[ operation, status, created_at ]`, `[ operation, type, created_at ]`, `[ status, type, created_at ]`, `[ file_migration_id, operation, status, type ]`, `[ file_migration_id, operation, status, created_at ]`, `[ file_migration_id, operation, type, created_at ]`, `[ file_migration_id, status, type, created_at ]`, `[ operation, status, type, created_at ]` or `[ file_migration_id, operation, status, type, created_at ]`.

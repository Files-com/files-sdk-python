# FileAction

## Example FileAction Object

```
{
  "status": "enqueued",
  "file_migration_id": "123"
}
```

* `status` (string): Status of file operation. Possible values: completed, enqueued.
* `file_migration_id` (int64): If status is enqueued, this is the id of the FileMigration to check for status updates.

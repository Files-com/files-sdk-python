# FileAction

## Example FileAction Object

```
{
  "status": "pending",
  "file_migration_id": 1
}
```

* `status` (string): Status of file operation.
* `file_migration_id` (int64): If status is pending, this is the id of the File Migration to check for status updates.  Delete actions include it whenever the deletion runs as a File Migration, including while it is processing.

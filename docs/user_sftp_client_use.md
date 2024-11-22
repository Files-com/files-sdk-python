# UserSftpClientUse

## Example UserSftpClientUse Object

```
{
  "id": 1,
  "sftp_client": "example",
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z",
  "user_id": 1
}
```

* `id` (int64): UserSftpClientUse ID
* `sftp_client` (string): The SFTP client used
* `created_at` (date-time): The earliest recorded use of this SFTP client (for this user)
* `updated_at` (date-time): The most recent use of this SFTP client (for this user)
* `user_id` (int64): ID of the user who performed this access


---

## List User SFTP Client Uses

```
files_sdk.user_sftp_client_use.list({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).


---

## Create an export CSV of User SFTP Client Use resources

```
files_sdk.user_sftp_client_use.create_export({
  "user_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  Provide a value of `0` to operate the current session's user.

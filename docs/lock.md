# Lock

## Example Lock Object

The API sends each `Lock` record as JSON, such as:

```json
{
  "path": "locked_file",
  "timeout": 1,
  "depth": "infinity",
  "recursive": true,
  "owner": "user",
  "scope": "shared",
  "exclusive": false,
  "token": "17c54824e9931a4688ca032d03f6663c",
  "type": "write",
  "allow_access_by_any_user": false,
  "user_id": 1,
  "username": ""
}
```

* `path` (string): Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `timeout` (int64): Lock timeout in seconds
* `depth` (string): 
* `recursive` (boolean): Does lock apply to subfolders?
* `owner` (string): Arbitrary descriptive label for the lock. Does not change the lock creator or permissions.
* `scope` (string): 
* `exclusive` (boolean): Is lock exclusive?
* `token` (string): Lock token.  Use to release lock.
* `type` (string): 
* `allow_access_by_any_user` (boolean): Can lock be modified by users other than its creator?
* `user_id` (int64): Lock creator user ID
* `username` (string): Lock creator username
* `expected_token` (string): Require this existing, unexpired token before refreshing or replacing a lock. Set token to the same value to refresh, or a different value to replace.

The functions below use the module's settings. Each is also a method of a client's
`client.lock` resource, such as
`client.lock.list_for(...)`,
which uses that client's configuration instead.


---

## List Locks by Path

```python
files_sdk.lock.list_for(path, {
  "include_children": False
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `path` (string): Required - Path to operate on.
* `include_children` (boolean): Include locks from children objects?


---

## Create Lock

```python
files_sdk.lock.create(path, {
  "token": "17c54824e9931a4688ca032d03f6663c",
  "allow_access_by_any_user": False,
  "exclusive": False,
  "recursive": True,
  "owner": "user",
  "timeout": 1
})
```

### Parameters

* `path` (string): Required - Path
* `token` (string): Lock token. With expected_token, use the same value to refresh or a different value to replace the existing token.
* `expected_token` (string): Require this existing, unexpired token before refreshing or replacing a lock. Set token to the same value to refresh, or a different value to replace.
* `allow_access_by_any_user` (boolean): Can lock be modified by users other than its creator?
* `exclusive` (boolean): Is lock exclusive?
* `recursive` (boolean): Does lock apply to subfolders?
* `owner` (string): Arbitrary descriptive label for the lock. Does not change the lock creator or permissions.
* `timeout` (int64): Lock timeout in seconds


---

## Delete Lock

```python
files_sdk.lock.delete(path, {
  "token": "token"
})
```

### Parameters

* `path` (string): Required - Path
* `token` (string): Required - Lock token


---

## Delete Lock

```python
lock = next(files_sdk.lock.list_for(path).auto_paging_iter(), None)
if lock is not None:
    lock.delete({
      "token": "token"
    })
```

### Parameters

* `path` (string): Required - Path
* `token` (string): Required - Lock token

# Lock

## Example Lock Object

```
{
  "path": "locked_file",
  "timeout": 43200,
  "depth": "infinity",
  "recursive": True,
  "owner": "user",
  "scope": "shared",
  "exclusive": True,
  "token": "17c54824e9931a4688ca032d03f6663c",
  "type": "write",
  "allow_access_by_any_user": True,
  "user_id": 1,
  "username": ""
}
```

* `path` (string): Path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `timeout` (int64): Lock timeout in seconds
* `depth` (string): DEPRECATED: Lock depth
* `recursive` (boolean): Does lock apply to subfolders?
* `owner` (string): Owner of the lock.  This can be any arbitrary string.
* `scope` (string): DEPRECATED: Lock scope
* `exclusive` (boolean): Is lock exclusive?
* `token` (string): Lock token.  Use to release lock.
* `type` (string): DEPRECATED: Lock type
* `allow_access_by_any_user` (boolean): Can lock be modified by users other than its creator?
* `user_id` (int64): Lock creator user ID
* `username` (string): Lock creator username


---

## List Locks by path

```
files_sdk.lock.list_for(path, {
  "per_page": 1,
  "include_children": True
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `path` (string): Required - Path to operate on.
* `include_children` (boolean): Include locks from children objects?


---

## Create Lock

```
files_sdk.lock.create(path, {
  "allow_access_by_any_user": True,
  "exclusive": True,
  "recursive": True,
  "timeout": 1
})
```

### Parameters

* `path` (string): Required - Path
* `allow_access_by_any_user` (boolean): Allow lock to be updated by any user?
* `exclusive` (boolean): Is lock exclusive?
* `recursive` (string): Does lock apply to subfolders?
* `timeout` (int64): Lock timeout length


---

## Delete Lock

```
files_sdk.lock.delete(path, {
  "token": "token"
})
```

### Parameters

* `path` (string): Required - Path
* `token` (string): Required - Lock token


---

## Delete Lock

```
lock = files_sdk.lock.list.first
lock.delete({
  "token": "token"
})
```

### Parameters

* `path` (string): Required - Path
* `token` (string): Required - Lock token

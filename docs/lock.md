# Lock

## Example Lock Object

```
{
  "path": "locked_file",
  "timeout": 43200,
  "depth": "infinity",
  "owner": "user",
  "scope": "shared",
  "token": "17c54824e9931a4688ca032d03f6663c",
  "type": "write",
  "user_id": 1,
  "username": ""
}
```

* `path` (string): Path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `timeout` (int64): Lock timeout
* `depth` (string): Lock depth (0 or infinity)
* `owner` (string): Owner of lock.  This can be any arbitrary string.
* `scope` (string): Lock scope(shared or exclusive)
* `token` (string): Lock token.  Use to release lock.
* `type` (string): Lock type
* `user_id` (int64): Lock creator user ID
* `username` (string): Lock creator username


---

## List Locks by path

```
files_sdk.lock.list_for(path, {
  "page": 1,
  "per_page": 1,
  "include_children": True
})
```

### Parameters

* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
* `cursor` (string): Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `path` (string): Required - Path to operate on.
* `include_children` (boolean): Include locks from children objects?


---

## Create Lock

```
files_sdk.lock.create(path, {
  "timeout": 1
})
```

### Parameters

* `path` (string): Required - Path
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
lock = files_sdk.lock.list_for(path).first

lock.delete({
  "token": "token"
})
```

### Parameters

* `path` (string): Required - Path
* `token` (string): Required - Lock token

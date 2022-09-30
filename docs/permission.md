# Permission

## Example Permission Object

```
{
  "id": 1,
  "path": "example",
  "user_id": 1,
  "username": "Sser",
  "group_id": 1,
  "group_name": "example",
  "permission": "full",
  "recursive": True
}
```

* `id` (int64): Permission ID
* `path` (string): Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `user_id` (int64): User ID
* `username` (string): User's username
* `group_id` (int64): Group ID
* `group_name` (string): Group name if applicable
* `permission` (string): Permission type
* `recursive` (boolean): Does this permission apply to subfolders?


---

## List Permissions

```
files_sdk.permission.list({
  "per_page": 1,
  "path": "example",
  "group_id": 1,
  "user_id": 1,
  "include_groups": True
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `group_id`, `path`, `user_id` or `permission`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `group_id`, `user_id` or `path`. Valid field combinations are `[ group_id, path ]` and `[ user_id, path ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `group_id`, `user_id` or `path`. Valid field combinations are `[ group_id, path ]` and `[ user_id, path ]`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `group_id`, `user_id` or `path`. Valid field combinations are `[ group_id, path ]` and `[ user_id, path ]`.
* `filter_like` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `group_id`, `user_id` or `path`. Valid field combinations are `[ group_id, path ]` and `[ user_id, path ]`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `group_id`, `user_id` or `path`. Valid field combinations are `[ group_id, path ]` and `[ user_id, path ]`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `group_id`, `user_id` or `path`. Valid field combinations are `[ group_id, path ]` and `[ user_id, path ]`.
* `path` (string): DEPRECATED: Permission path.  If provided, will scope permissions to this path. Use `filter[path]` instead.
* `group_id` (string): DEPRECATED: Group ID.  If provided, will scope permissions to this group. Use `filter[group_id]` instead.`
* `user_id` (string): DEPRECATED: User ID.  If provided, will scope permissions to this user. Use `filter[user_id]` instead.`
* `include_groups` (boolean): If searching by user or group, also include user's permissions that are inherited from its groups?


---

## Create Permission

```
files_sdk.permission.create({
  "group_id": 1,
  "path": "example",
  "permission": "full",
  "recursive": True,
  "user_id": 1,
  "username": "Sser"
})
```

### Parameters

* `group_id` (int64): Group ID
* `path` (string): Folder path
* `permission` (string):  Permission type.  Can be `admin`, `full`, `readonly`, `writeonly`, `list`, or `history`
* `recursive` (boolean): Apply to subfolders recursively?
* `user_id` (int64): User ID.  Provide `username` or `user_id`
* `username` (string): User username.  Provide `username` or `user_id`


---

## Delete Permission

```
files_sdk.permission.delete(id)
```

### Parameters

* `id` (int64): Required - Permission ID.


---

## Delete Permission

```
permission = files_sdk.permission.list.first
permission.delete()
```

### Parameters

* `id` (int64): Required - Permission ID.

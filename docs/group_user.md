# GroupUser

## Example GroupUser Object

```
{
  "group_name": "My Group",
  "group_id": 1,
  "user_id": 1,
  "admin": True,
  "usernames": [

  ]
}
```

* `group_name` (string): Group name
* `group_id` (int64): Group ID
* `user_id` (int64): User ID
* `admin` (boolean): Is this user an administrator of this group?
* `usernames` (array): A list of usernames for users in this group
* `id` (int64): Group User ID.


---

## List Group Users

```
files_sdk.group_user.list({
  "user_id": 1,
  "page": 1,
  "per_page": 1,
  "group_id": 1
})
```

### Parameters

* `user_id` (int64): User ID.  If provided, will return group_users of this user.
* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
* `cursor` (string): Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `group_id` (int64): Group ID.  If provided, will return group_users of this group.


---

## Update Group User

```
files_sdk.group_user.update(id, {
  "group_id": 1,
  "user_id": 1,
  "admin": True
})
```

### Parameters

* `id` (int64): Required - Group User ID.
* `group_id` (int64): Required - Group ID to add user to.
* `user_id` (int64): Required - User ID to add to group.
* `admin` (boolean): Is the user a group administrator?


---

## Delete Group User

```
files_sdk.group_user.delete(id, {
  "group_id": 1,
  "user_id": 1
})
```

### Parameters

* `id` (int64): Required - Group User ID.
* `group_id` (int64): Required - Group ID from which to remove user.
* `user_id` (int64): Required - User ID to remove from group.


---

## Update Group User

```
group_user = files_sdk.group_user.list_for(path).first

group_user.update({
  "group_id": 1,
  "user_id": 1,
  "admin": True
})
```

### Parameters

* `id` (int64): Required - Group User ID.
* `group_id` (int64): Required - Group ID to add user to.
* `user_id` (int64): Required - User ID to add to group.
* `admin` (boolean): Is the user a group administrator?


---

## Delete Group User

```
group_user = files_sdk.group_user.list_for(path).first

group_user.delete({
  "group_id": 1,
  "user_id": 1
})
```

### Parameters

* `id` (int64): Required - Group User ID.
* `group_id` (int64): Required - Group ID from which to remove user.
* `user_id` (int64): Required - User ID to remove from group.

# GroupUser

## Example GroupUser Object

The API sends each `GroupUser` record as JSON, such as:

```json
{
  "group_name": "My Group",
  "group_id": 1,
  "user_id": 1,
  "admin": true,
  "username": "example"
}
```

* `group_name` (string): Group name
* `group_id` (int64): Group ID
* `user_id` (int64): User ID
* `admin` (boolean): Is this user an administrator of this group?
* `username` (string): Username of the user
* `id` (int64): Group User ID.

The functions below use the module's settings. Each is also a method of a client's
`client.group_user` resource, such as
`client.group_user.list(...)`,
which uses that client's configuration instead.


---

## List Group Users

```python
files_sdk.group_user.list({
  "group_id": 1,
  "user_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `group_id` (int64): Group ID. If provided, returns memberships of this group. Requires a Site Administrator, a Read-only Administrator, a Workspace Administrator for the group's workspace, or a Group Administrator of this group.
* `user_id` (int64): User ID.  If provided, will return group_users of this user.


---

## Create Group User

```python
files_sdk.group_user.create({
  "group_id": 1,
  "user_id": 1,
  "admin": False
})
```

### Parameters

* `group_id` (int64): Required - Group ID to add user to.
* `user_id` (int64): Required - User ID to add to group.
* `admin` (boolean): Is the user a group administrator?


---

## Update Group User

```python
files_sdk.group_user.update(id, {
  "group_id": 1,
  "user_id": 1,
  "admin": False
})
```

### Parameters

* `id` (int64): Required - Group User ID.
* `group_id` (int64): Required - Group ID to add user to.
* `user_id` (int64): Required - User ID to add to group.
* `admin` (boolean): Is the user a group administrator?


---

## Delete Group User

```python
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

A `GroupUser` record from the API does not include its `id`,
so set the `id` you already know before calling `update()`.

```python
group_user = files_sdk.group_user.new()
group_user.id = id
group_user.update({
  "group_id": 1,
  "user_id": 1,
  "admin": False
})
```

### Parameters

* `id` (int64): Required - Group User ID.
* `group_id` (int64): Required - Group ID to add user to.
* `user_id` (int64): Required - User ID to add to group.
* `admin` (boolean): Is the user a group administrator?


---

## Delete Group User

A `GroupUser` record from the API does not include its `id`,
so set the `id` you already know before calling `delete()`.

```python
group_user = files_sdk.group_user.new()
group_user.id = id
group_user.delete({
  "group_id": 1,
  "user_id": 1
})
```

### Parameters

* `id` (int64): Required - Group User ID.
* `group_id` (int64): Required - Group ID from which to remove user.
* `user_id` (int64): Required - User ID to remove from group.

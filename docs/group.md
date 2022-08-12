# Group

## Example Group Object

```
{
  "id": 1,
  "name": "owners",
  "admin_ids": "1",
  "notes": "",
  "user_ids": "1",
  "usernames": "user"
}
```

* `id` (int64): Group ID
* `name` (string): Group name
* `admin_ids` (string): Comma-delimited list of user IDs who are group administrators (separated by commas)
* `notes` (string): Notes about this group
* `user_ids` (string): Comma-delimited list of user IDs who belong to this group (separated by commas)
* `usernames` (string): Comma-delimited list of usernames who belong to this group (separated by commas)


---

## List Groups

```
files_sdk.group.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `name`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `name`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal to the supplied value. Valid fields are `name`.
* `filter_like` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `name`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `name`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal to the supplied value. Valid fields are `name`.
* `ids` (string): Comma-separated list of group ids to include in results.


---

## Show Group

```
files_sdk.group.find(id)
```

### Parameters

* `id` (int64): Required - Group ID.


---

## Create Group

```
files_sdk.group.create({
  "name": "owners",
  "user_ids": "1",
  "admin_ids": "1"
})
```

### Parameters

* `name` (string): Group name.
* `notes` (string): Group notes.
* `user_ids` (string): A list of user ids. If sent as a string, should be comma-delimited.
* `admin_ids` (string): A list of group admin user ids. If sent as a string, should be comma-delimited.


---

## Update Group

```
files_sdk.group.update(id, {
  "name": "owners",
  "user_ids": "1",
  "admin_ids": "1"
})
```

### Parameters

* `id` (int64): Required - Group ID.
* `name` (string): Group name.
* `notes` (string): Group notes.
* `user_ids` (string): A list of user ids. If sent as a string, should be comma-delimited.
* `admin_ids` (string): A list of group admin user ids. If sent as a string, should be comma-delimited.


---

## Delete Group

```
files_sdk.group.delete(id)
```

### Parameters

* `id` (int64): Required - Group ID.


---

## Update Group

```
group = files_sdk.group.list.first
group.update({
  "name": "owners",
  "user_ids": "1",
  "admin_ids": "1"
})
```

### Parameters

* `id` (int64): Required - Group ID.
* `name` (string): Group name.
* `notes` (string): Group notes.
* `user_ids` (string): A list of user ids. If sent as a string, should be comma-delimited.
* `admin_ids` (string): A list of group admin user ids. If sent as a string, should be comma-delimited.


---

## Delete Group

```
group = files_sdk.group.list.first
group.delete()
```

### Parameters

* `id` (int64): Required - Group ID.

# Group

## Example Group Object

```
{
  "id": 1,
  "name": "owners",
  "admin_ids": "1",
  "notes": "example",
  "user_ids": "1",
  "usernames": "example"
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

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[name]=desc`). Valid fields are `name`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `name`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `name`.
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
  "notes": "example",
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
  "notes": "example",
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
  "notes": "example",
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

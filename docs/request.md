# Request

## Example Request Object

```
{
  "id": 1,
  "path": "",
  "source": "",
  "destination": "",
  "automation_id": "",
  "user_display_name": ""
}
```

* `id` (int64): Request ID
* `path` (string): Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `source` (string): Source filename, if applicable
* `destination` (string): Destination filename
* `automation_id` (string): ID of automation that created request
* `user_display_name` (string): User making the request (if applicable)
* `user_ids` (string): A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.


---

## List Requests

```
files_sdk.request.list({
  "per_page": 1,
  "mine": True
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `destination`.
* `mine` (boolean): Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
* `path` (string): Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.


---

## List Requests

```
files_sdk.request.get_folder(path, {
  "per_page": 1,
  "mine": True
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via either the X-Files-Cursor-Next header or the X-Files-Cursor-Prev header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `destination`.
* `mine` (boolean): Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
* `path` (string): Required - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.


---

## Create Request

```
files_sdk.request.create({
  "path": "path",
  "destination": "destination"
})
```

### Parameters

* `path` (string): Required - Folder path on which to request the file.
* `destination` (string): Required - Destination filename (without extension) to request.
* `user_ids` (string): A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.


---

## Delete Request

```
files_sdk.request.delete(id)
```

### Parameters

* `id` (int64): Required - Request ID.


---

## Delete Request

```
request = files_sdk.request.list.first
request.delete()
```

### Parameters

* `id` (int64): Required - Request ID.

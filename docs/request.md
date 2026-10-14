# Request

## Example Request Object

The API sends each `Request` record as JSON, such as:

```json
{
  "id": 1,
  "path": "example",
  "source": "example",
  "destination": "example",
  "automation_id": 1,
  "user_display_name": "example"
}
```

* `id` (int64): Request ID
* `path` (string): Folder path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `source` (string): Source filename, if applicable
* `destination` (string): Destination filename
* `automation_id` (int64): ID of automation that created request
* `user_display_name` (string): User making the request (if applicable)
* `user_ids` (string): A list of user IDs to request the file from. If sent as a string, it should be comma-delimited.
* `group_ids` (string): A list of group IDs to request the file from. If sent as a string, it should be comma-delimited.

The functions below use the module's settings. Each is also a method of a client's
`client.request` resource, such as
`client.request.list(...)`,
which uses that client's configuration instead.


---

## List Requests

```python
files_sdk.request.list({
  "mine": False,
  "path": "example"
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
* `mine` (boolean): Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
* `path` (string): Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.


---

## List Requests

```python
files_sdk.request.get_folder(path, {
  "mine": False
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are .
* `mine` (boolean): Only show requests of the current user?  (Defaults to true if current user is not a site admin.)
* `path` (string): Required - Path to show requests for.  If omitted, shows all paths. Send `/` to represent the root directory.


---

## Create Request

```python
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

```python
files_sdk.request.delete(id)
```

### Parameters

* `id` (int64): Required - Request ID.


---

## Delete Request

```python
request = next(files_sdk.request.list().auto_paging_iter(), None)
if request is not None:
    request.delete()
```

### Parameters

* `id` (int64): Required - Request ID.

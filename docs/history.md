# History

## Example History Object

```
{
  "id": 1,
  "path": "",
  "when": "2000-01-01T01:00:00Z",
  "destination": "/to_path",
  "display": "Actual text of the action here.",
  "ip": "192.283.128.182",
  "source": "/from_path",
  "targets": [

  ],
  "user_id": 1,
  "username": "user",
  "action": "create",
  "failure_type": "none",
  "interface": "web"
}
```

* `id` (int64): Action ID
* `path` (string): Path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `when` (date-time): Action occurrence date/time
* `destination` (string): The destination path for this action, if applicable
* `display` (string): Friendly displayed output
* `ip` (string): IP Address that performed this action
* `source` (string): The source path for this action, if applicable
* `targets` (array(object)): Targets
* `user_id` (int64): User ID
* `username` (string): Username
* `action` (string): Type of action
* `failure_type` (string): Failure type.  If action was a user login or session failure, why did it fail?
* `interface` (string): Interface on which this action occurred.


---

## List history for specific file

```
files_sdk.history.list_for_file(path, {
  "display": "Actual text of the action here.",
  "per_page": 1,
  "action": "create",
  "page": 1
})
```

### Parameters

* `start_at` (string): Leave blank or set to a date/time to filter earlier entries.
* `end_at` (string): Leave blank or set to a date/time to filter later entries.
* `display` (string): Display format. Leave blank or set to `full` or `parent`.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[user_id]=desc`). Valid fields are `user_id` and `created_at`.
* `path` (string): Required - Path to operate on.


---

## List history for specific folder

```
files_sdk.history.list_for_folder(path, {
  "display": "Actual text of the action here.",
  "per_page": 1,
  "action": "create",
  "page": 1
})
```

### Parameters

* `start_at` (string): Leave blank or set to a date/time to filter earlier entries.
* `end_at` (string): Leave blank or set to a date/time to filter later entries.
* `display` (string): Display format. Leave blank or set to `full` or `parent`.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[user_id]=desc`). Valid fields are `user_id` and `created_at`.
* `path` (string): Required - Path to operate on.


---

## List history for specific user

```
files_sdk.history.list_for_user(user_id, {
  "display": "Actual text of the action here.",
  "per_page": 1,
  "action": "create",
  "page": 1
})
```

### Parameters

* `start_at` (string): Leave blank or set to a date/time to filter earlier entries.
* `end_at` (string): Leave blank or set to a date/time to filter later entries.
* `display` (string): Display format. Leave blank or set to `full` or `parent`.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[user_id]=desc`). Valid fields are `user_id` and `created_at`.
* `user_id` (int64): Required - User ID.


---

## List site login history

```
files_sdk.history.list_logins({
  "display": "Actual text of the action here.",
  "per_page": 1,
  "action": "create",
  "page": 1
})
```

### Parameters

* `start_at` (string): Leave blank or set to a date/time to filter earlier entries.
* `end_at` (string): Leave blank or set to a date/time to filter later entries.
* `display` (string): Display format. Leave blank or set to `full` or `parent`.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[user_id]=desc`). Valid fields are `user_id` and `created_at`.


---

## List site full action history

```
files_sdk.history.list({
  "display": "Actual text of the action here.",
  "per_page": 1,
  "action": "create",
  "page": 1
})
```

### Parameters

* `start_at` (string): Leave blank or set to a date/time to filter earlier entries.
* `end_at` (string): Leave blank or set to a date/time to filter later entries.
* `display` (string): Display format. Leave blank or set to `full` or `parent`.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[path]=desc`). Valid fields are `path`, `folder`, `user_id` or `created_at`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `user_id`, `folder` or `path`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.

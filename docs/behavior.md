# Behavior

## Example Behavior Object

```
{
  "id": 1,
  "path": "example",
  "attachment_url": "example",
  "behavior": "webhook",
  "name": "example",
  "description": "example",
  "value": {
    "key": "example value"
  },
  "disable_parent_folder_behavior": True,
  "recursive": True
}
```

* `id` (int64): Folder behavior ID
* `path` (string): Folder path.  Note that Behavior paths cannot be updated once initially set.  You will need to remove and re-create the behavior on the new path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `attachment_url` (string): URL for attached file
* `behavior` (string): Behavior type.
* `name` (string): Name for this behavior.
* `description` (string): Description for this behavior.
* `value` (object): Settings for this behavior.  See the section above for an example value to provide here.  Formatting is different for each Behavior type.  May be sent as nested JSON or a single JSON-encoded string.  If using XML encoding for the API call, this data must be sent as a JSON-encoded string.
* `disable_parent_folder_behavior` (boolean): If true, the parent folder's behavior will be disabled for this folder and its children.
* `recursive` (boolean): Is behavior recursive?
* `attachment_file` (file): Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
* `attachment_delete` (boolean): If `true`, delete the file stored in `attachment`.


---

## List Behaviors

```
files_sdk.behavior.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `behavior` and `impacts_ui`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `impacts_ui` and `behavior`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `behavior`.


---

## Show Behavior

```
files_sdk.behavior.find(id)
```

### Parameters

* `id` (int64): Required - Behavior ID.


---

## List Behaviors by path

```
files_sdk.behavior.list_for(path, {
  "ancestor_behaviors": True
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `behavior` and `impacts_ui`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `impacts_ui` and `behavior`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `behavior`.
* `path` (string): Required - Path to operate on.
* `ancestor_behaviors` (boolean): If `true`, behaviors above this path are shown.


---

## Create Behavior

```
files_sdk.behavior.create({
  "value": "{\"method\": \"GET\"}",
  "disable_parent_folder_behavior": True,
  "recursive": True,
  "name": "example",
  "description": "example",
  "path": "path",
  "behavior": "webhook"
})
```

### Parameters

* `value` (string): This field stores a hash of data specific to the type of behavior. See The Behavior Types section for example values for each type of behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
* `disable_parent_folder_behavior` (boolean): If `true`, the parent folder's behavior will be disabled for this folder and its children. This is the main mechanism for canceling out a `recursive` behavior higher in the folder tree.
* `recursive` (boolean): If `true`, behavior is treated as recursive, meaning that it impacts child folders as well.
* `name` (string): Name for this behavior.
* `description` (string): Description for this behavior.
* `path` (string): Required - Path where this behavior should apply.
* `behavior` (string): Required - Behavior type.


---

## Test webhook

```
files_sdk.behavior.webhook_test({
  "url": "https://www.site.com/...",
  "method": "GET",
  "encoding": "RAW",
  "headers": {"x-test-header":"testvalue"},
  "body": {"test-param":"testvalue"}
})
```

### Parameters

* `url` (string): Required - URL for testing the webhook.
* `method` (string): HTTP request method (GET or POST).
* `encoding` (string): Encoding type for the webhook payload. Can be JSON, XML, or RAW (form data).
* `headers` (object): Additional request headers to send via HTTP.
* `body` (object): Additional body parameters to include in the webhook payload.
* `action` (string): Action for test body.


---

## Update Behavior

```
files_sdk.behavior.update(id, {
  "value": "{\"method\": \"GET\"}",
  "disable_parent_folder_behavior": True,
  "recursive": True,
  "name": "example",
  "description": "example",
  "attachment_delete": True
})
```

### Parameters

* `id` (int64): Required - Behavior ID.
* `value` (string): This field stores a hash of data specific to the type of behavior. See The Behavior Types section for example values for each type of behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
* `disable_parent_folder_behavior` (boolean): If `true`, the parent folder's behavior will be disabled for this folder and its children. This is the main mechanism for canceling out a `recursive` behavior higher in the folder tree.
* `recursive` (boolean): If `true`, behavior is treated as recursive, meaning that it impacts child folders as well.
* `name` (string): Name for this behavior.
* `description` (string): Description for this behavior.
* `attachment_delete` (boolean): If `true`, delete the file stored in `attachment`.


---

## Delete Behavior

```
files_sdk.behavior.delete(id)
```

### Parameters

* `id` (int64): Required - Behavior ID.


---

## Update Behavior

```
behavior = files_sdk.behavior.find(id)
behavior.update({
  "value": "{\"method\": \"GET\"}",
  "disable_parent_folder_behavior": True,
  "recursive": True,
  "name": "example",
  "description": "example",
  "attachment_delete": True
})
```

### Parameters

* `id` (int64): Required - Behavior ID.
* `value` (string): This field stores a hash of data specific to the type of behavior. See The Behavior Types section for example values for each type of behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the `watermark` behavior requires a watermark image. Attach that file here.
* `disable_parent_folder_behavior` (boolean): If `true`, the parent folder's behavior will be disabled for this folder and its children. This is the main mechanism for canceling out a `recursive` behavior higher in the folder tree.
* `recursive` (boolean): If `true`, behavior is treated as recursive, meaning that it impacts child folders as well.
* `name` (string): Name for this behavior.
* `description` (string): Description for this behavior.
* `attachment_delete` (boolean): If `true`, delete the file stored in `attachment`.


---

## Delete Behavior

```
behavior = files_sdk.behavior.find(id)
behavior.delete()
```

### Parameters

* `id` (int64): Required - Behavior ID.

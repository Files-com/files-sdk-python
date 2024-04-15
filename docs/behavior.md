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
  "disable_parent_folder_behavior": True
}
```

* `id` (int64): Folder behavior ID
* `path` (string): Folder path.  Note that Behavior paths cannot be updated once initially set.  You will need to remove and re-create the behavior on the new path. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `attachment_url` (string): URL for attached file
* `behavior` (string): Behavior type.
* `name` (string): Name for this behavior.
* `description` (string): Description for this behavior.
* `value` (object): Settings for this behavior.  See the section above for an example value to provide here.  Formatting is different for each Behavior type.  May be sent as nested JSON or a single JSON-encoded string.  If using XML encoding for the API call, this data must be sent as a JSON-encoded string.
* `disable_parent_folder_behavior` (boolean): If true, the parent folder's behavior will be disabled for this folder.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
* `attachment_delete` (boolean): If true, will delete the file stored in attachment


---

## List Behaviors

```
files_sdk.behavior.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[behavior]=desc`). Valid fields are `behavior`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `behavior`.
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
  "per_page": 1,
  "behavior": "webhook"
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[behavior]=desc`). Valid fields are `behavior`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `behavior`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `behavior`.
* `path` (string): Required - Path to operate on.
* `recursive` (string): Show behaviors above this path?
* `behavior` (string): DEPRECATED: If set only shows folder behaviors matching this behavior type. Use `filter[behavior]` instead.


---

## Create Behavior

```
files_sdk.behavior.create({
  "value": "{\"method\": \"GET\"}",
  "name": "example",
  "description": "example",
  "path": "path",
  "behavior": "webhook"
})
```

### Parameters

* `value` (string): The value of the folder behavior.  Can be an integer, array, or hash depending on the type of folder behavior. See The Behavior Types section for example values for each type of behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
* `name` (string): Name for this behavior.
* `description` (string): Description for this behavior.
* `path` (string): Required - Folder behaviors path.
* `behavior` (string): Required - Behavior type.


---

## Test webhook

```
files_sdk.behavior.webhook_test({
  "url": "https://www.site.com/...",
  "method": "GET",
  "encoding": "RAW",
  "headers": {"x-test-header":"testvalue"},
  "body": {"test-param":"testvalue"},
  "action": "test"
})
```

### Parameters

* `url` (string): Required - URL for testing the webhook.
* `method` (string): HTTP method(GET or POST).
* `encoding` (string): HTTP encoding method.  Can be JSON, XML, or RAW (form data).
* `headers` (object): Additional request headers.
* `body` (object): Additional body parameters.
* `action` (string): action for test body


---

## Update Behavior

```
files_sdk.behavior.update(id, {
  "value": "{\"method\": \"GET\"}",
  "name": "example",
  "description": "example",
  "behavior": "webhook",
  "path": "example",
  "attachment_delete": True
})
```

### Parameters

* `id` (int64): Required - Behavior ID.
* `value` (string): The value of the folder behavior.  Can be an integer, array, or hash depending on the type of folder behavior. See The Behavior Types section for example values for each type of behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
* `name` (string): Name for this behavior.
* `description` (string): Description for this behavior.
* `behavior` (string): Behavior type.
* `path` (string): Folder behaviors path.
* `attachment_delete` (boolean): If true, will delete the file stored in attachment


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
behavior = files_sdk.behavior.list.first
behavior.update({
  "value": "{\"method\": \"GET\"}",
  "name": "example",
  "description": "example",
  "behavior": "webhook",
  "path": "example",
  "attachment_delete": True
})
```

### Parameters

* `id` (int64): Required - Behavior ID.
* `value` (string): The value of the folder behavior.  Can be an integer, array, or hash depending on the type of folder behavior. See The Behavior Types section for example values for each type of behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
* `name` (string): Name for this behavior.
* `description` (string): Description for this behavior.
* `behavior` (string): Behavior type.
* `path` (string): Folder behaviors path.
* `attachment_delete` (boolean): If true, will delete the file stored in attachment


---

## Delete Behavior

```
behavior = files_sdk.behavior.list.first
behavior.delete()
```

### Parameters

* `id` (int64): Required - Behavior ID.

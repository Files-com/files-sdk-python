# Behavior

## Example Behavior Object

```
{
  "id": 1,
  "path": "",
  "attachment_url": "",
  "behavior": "webhook",
  "value": {
    "method": "GET"
  }
}
```

* `id` (int64): Folder behavior ID
* `path` (string): Folder path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `attachment_url` (string): URL for attached file
* `behavior` (string): Behavior type.
* `value` (object): Settings for this behavior.  See the section above for an example value to provide here.  Formatting is different for each Behavior type.  May be sent as nested JSON or a single JSON-encoded string.  If using XML encoding for the API call, this data must be sent as a JSON-encoded string.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image


---

## List Behaviors

```
files_sdk.behavior.list({
  "per_page": 1,
  "behavior": "webhook"
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `behavior`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `behavior`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `behavior`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `behavior`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `behavior`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `behavior`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `behavior`.
* `behavior` (string): If set, only shows folder behaviors matching this behavior type.


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

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `behavior`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `behavior`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `behavior`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `behavior`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `behavior`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `behavior`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `behavior`.
* `path` (string): Required - Path to operate on.
* `recursive` (string): Show behaviors above this path?
* `behavior` (string): DEPRECATED: If set only shows folder behaviors matching this behavior type. Use `filter[behavior]` instead.


---

## Create Behavior

```
files_sdk.behavior.create({
  "value": "{\"method\": \"GET\"}",
  "path": "path",
  "behavior": "webhook"
})
```

### Parameters

* `value` (string): The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
* `path` (string): Required - Folder behaviors path.
* `behavior` (string): Required - Behavior type.


---

## Test webhook

```
files_sdk.behavior.webhook_test({
  "url": "https://www.site.com/...",
  "method": "GET",
  "encoding": "RAW",
  "headers": "x-test-header => testvalue",
  "body": "test-param => testvalue",
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
  "behavior": "webhook"
})
```

### Parameters

* `id` (int64): Required - Behavior ID.
* `value` (string): The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
* `behavior` (string): Behavior type.
* `path` (string): Folder behaviors path.


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
behavior = files_sdk.behavior.find(1)

behavior.update({
  "value": "{\"method\": \"GET\"}",
  "behavior": "webhook"
})
```

### Parameters

* `id` (int64): Required - Behavior ID.
* `value` (string): The value of the folder behavior.  Can be a integer, array, or hash depending on the type of folder behavior.
* `attachment_file` (file): Certain behaviors may require a file, for instance, the "watermark" behavior requires a watermark image
* `behavior` (string): Behavior type.
* `path` (string): Folder behaviors path.


---

## Delete Behavior

```
behavior = files_sdk.behavior.find(1)

behavior.delete()
```

### Parameters

* `id` (int64): Required - Behavior ID.

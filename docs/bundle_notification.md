# BundleNotification

## Example BundleNotification Object

```
{
  "bundle_id": 1,
  "id": 1,
  "notify_on_registration": True,
  "notify_on_upload": True,
  "user_id": 1
}
```

* `bundle_id` (int64): Bundle ID to notify on
* `id` (int64): Bundle Notification ID
* `notify_on_registration` (boolean): Triggers bundle notification when a registration action occurs for it.
* `notify_on_upload` (boolean): Triggers bundle notification when a upload action occurs for it.
* `user_id` (int64): The id of the user to notify.


---

## List Bundle Notifications

```
files_sdk.bundle_notification.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `bundle_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `bundle_id`.


---

## Show Bundle Notification

```
files_sdk.bundle_notification.find(id)
```

### Parameters

* `id` (int64): Required - Bundle Notification ID.


---

## Create Bundle Notification

```
files_sdk.bundle_notification.create({
  "bundle_id": 1,
  "user_id": 1,
  "notify_on_registration": True,
  "notify_on_upload": True
})
```

### Parameters

* `bundle_id` (int64): Required - Bundle ID to notify on
* `user_id` (int64): The id of the user to notify.
* `notify_on_registration` (boolean): Triggers bundle notification when a registration action occurs for it.
* `notify_on_upload` (boolean): Triggers bundle notification when a upload action occurs for it.


---

## Create Export Bundle Notification

```
files_sdk.bundle_notification.create_export()
```

### Parameters

* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `bundle_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `bundle_id`.


---

## Update Bundle Notification

```
files_sdk.bundle_notification.update(id, {
  "notify_on_registration": True,
  "notify_on_upload": True
})
```

### Parameters

* `id` (int64): Required - Bundle Notification ID.
* `notify_on_registration` (boolean): Triggers bundle notification when a registration action occurs for it.
* `notify_on_upload` (boolean): Triggers bundle notification when a upload action occurs for it.


---

## Delete Bundle Notification

```
files_sdk.bundle_notification.delete(id)
```

### Parameters

* `id` (int64): Required - Bundle Notification ID.


---

## Update Bundle Notification

```
bundle_notification = files_sdk.bundle_notification.find(id)
bundle_notification.update({
  "notify_on_registration": True,
  "notify_on_upload": True
})
```

### Parameters

* `id` (int64): Required - Bundle Notification ID.
* `notify_on_registration` (boolean): Triggers bundle notification when a registration action occurs for it.
* `notify_on_upload` (boolean): Triggers bundle notification when a upload action occurs for it.


---

## Delete Bundle Notification

```
bundle_notification = files_sdk.bundle_notification.find(id)
bundle_notification.delete()
```

### Parameters

* `id` (int64): Required - Bundle Notification ID.

# Notification

## Example Notification Object

```
{
  "id": 1,
  "path": "",
  "group_id": 1,
  "group_name": "",
  "notify_user_actions": True,
  "notify_on_copy": True,
  "send_interval": "fifteen_minutes",
  "unsubscribed": True,
  "unsubscribed_reason": "",
  "user_id": 1,
  "username": "User",
  "suppressed_email": True
}
```

* `id` (int64): Notification ID
* `path` (string): Folder path to notify on This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `group_id` (int64): Notification group id
* `group_name` (string): Group name if applicable
* `notify_user_actions` (boolean): Trigger notification on notification user actions?
* `notify_on_copy` (boolean): Triggers notification when moving or copying files to this path
* `send_interval` (string): The time interval that notifications are aggregated to
* `unsubscribed` (boolean): Is the user unsubscribed from this notification?
* `unsubscribed_reason` (string): The reason that the user unsubscribed
* `user_id` (int64): Notification user ID
* `username` (string): Notification username
* `suppressed_email` (boolean): If true, it means that the recipient at this user's email address has manually unsubscribed from all emails, or had their email "hard bounce", which means that we are unable to send mail to this user's current email address. Notifications will resume if the user changes their email address.


---

## List Notifications

```
files_sdk.notification.list({
  "user_id": 1,
  "page": 1,
  "per_page": 1,
  "group_id": 1,
  "include_ancestors": True
})
```

### Parameters

* `user_id` (int64): DEPRECATED: Show notifications for this User ID. Use `filter[user_id]` instead.
* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
* `cursor` (string): Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `site_id`, `path`, `user_id` or `group_id`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `user_id`, `group_id` or `path`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `user_id`, `group_id` or `path`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `user_id`, `group_id` or `path`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `user_id`, `group_id` or `path`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `user_id`, `group_id` or `path`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `user_id`, `group_id` or `path`.
* `group_id` (int64): DEPRECATED: Show notifications for this Group ID. Use `filter[group_id]` instead.
* `path` (string): Show notifications for this Path.
* `include_ancestors` (boolean): If `include_ancestors` is `true` and `path` is specified, include notifications for any parent paths. Ignored if `path` is not specified.


---

## Show Notification

```
files_sdk.notification.find(id)
```

### Parameters

* `id` (int64): Required - Notification ID.


---

## Create Notification

```
files_sdk.notification.create({
  "user_id": 1,
  "notify_on_copy": True,
  "notify_user_actions": True,
  "send_interval": "daily",
  "group_id": 1,
  "username": "User"
})
```

### Parameters

* `user_id` (int64): The id of the user to notify. Provide `user_id`, `username` or `group_id`.
* `notify_on_copy` (boolean): If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
* `notify_user_actions` (boolean): If `true` actions initiated by the user will still result in a notification
* `send_interval` (string): The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
* `group_id` (int64): The ID of the group to notify.  Provide `user_id`, `username` or `group_id`.
* `path` (string): Path
* `username` (string): The username of the user to notify.  Provide `user_id`, `username` or `group_id`.


---

## Update Notification

```
files_sdk.notification.update(id, {
  "notify_on_copy": True,
  "notify_user_actions": True,
  "send_interval": "daily"
})
```

### Parameters

* `id` (int64): Required - Notification ID.
* `notify_on_copy` (boolean): If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
* `notify_user_actions` (boolean): If `true` actions initiated by the user will still result in a notification
* `send_interval` (string): The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.


---

## Delete Notification

```
files_sdk.notification.delete(id)
```

### Parameters

* `id` (int64): Required - Notification ID.


---

## Update Notification

```
notification = files_sdk.notification.find(1)

notification.update({
  "notify_on_copy": True,
  "notify_user_actions": True,
  "send_interval": "daily"
})
```

### Parameters

* `id` (int64): Required - Notification ID.
* `notify_on_copy` (boolean): If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
* `notify_user_actions` (boolean): If `true` actions initiated by the user will still result in a notification
* `send_interval` (string): The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.


---

## Delete Notification

```
notification = files_sdk.notification.find(1)

notification.delete()
```

### Parameters

* `id` (int64): Required - Notification ID.

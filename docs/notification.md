# Notification

## Example Notification Object

```
{
  "id": 1,
  "path": "",
  "group_id": 1,
  "group_name": "example",
  "triggering_group_ids": [
    1
  ],
  "triggering_user_ids": [
    1
  ],
  "trigger_by_share_recipients": True,
  "notify_user_actions": True,
  "notify_on_copy": True,
  "notify_on_delete": True,
  "notify_on_download": True,
  "notify_on_move": True,
  "notify_on_upload": True,
  "recursive": True,
  "send_interval": "fifteen_minutes",
  "message": "custom notification email message",
  "triggering_filenames": [
    "*.jpg",
    "notify_file.txt"
  ],
  "unsubscribed": True,
  "unsubscribed_reason": "example",
  "user_id": 1,
  "username": "User",
  "suppressed_email": True
}
```

* `id` (int64): Notification ID
* `path` (string): Folder path to notify on This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `group_id` (int64): ID of Group to receive notifications
* `group_name` (string): Group name, if a Group ID is set
* `triggering_group_ids` (array): If set, will only notify on actions made by a member of one of the specified groups
* `triggering_user_ids` (array): If set, will onlynotify on actions made one of the specified users
* `trigger_by_share_recipients` (boolean): Notify when actions are performed by a share recipient?
* `notify_user_actions` (boolean): If true, will send notifications about a user's own activity to that user.  If false, only activity performed by other users (or anonymous users) will be sent in notifications.
* `notify_on_copy` (boolean): Trigger on files copied to this path?
* `notify_on_delete` (boolean): Trigger on files deleted in this path?
* `notify_on_download` (boolean): Trigger on files downloaded in this path?
* `notify_on_move` (boolean): Trigger on files moved to this path?
* `notify_on_upload` (boolean): Trigger on files created/uploaded/updated/changed in this path?
* `recursive` (boolean): Apply notification recursively?  This will enable notifications for each subfolder.
* `send_interval` (string): The time interval that notifications are aggregated to
* `message` (string): Custom message to include in notification emails
* `triggering_filenames` (array): Array of filenames (possibly with wildcards) to scope trigger
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
  "per_page": 1,
  "include_ancestors": True,
  "group_id": 1
})
```

### Parameters

* `user_id` (int64): DEPRECATED: Show notifications for this User ID. Use `filter[user_id]` instead.
* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[path]=desc`). Valid fields are `path`, `user_id` or `group_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `path`, `user_id` or `group_id`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`.
* `path` (string): Show notifications for this Path.
* `include_ancestors` (boolean): If `include_ancestors` is `true` and `path` is specified, include notifications for any parent paths. Ignored if `path` is not specified.
* `group_id` (string): 


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
  "notify_on_delete": True,
  "notify_on_download": True,
  "notify_on_move": True,
  "notify_on_upload": True,
  "notify_user_actions": True,
  "recursive": True,
  "send_interval": "daily",
  "message": "custom notification email message",
  "triggering_filenames": ["*.jpg","notify_file.txt"],
  "triggering_group_ids": [1],
  "triggering_user_ids": [1],
  "trigger_by_share_recipients": True,
  "group_id": 1,
  "username": "User"
})
```

### Parameters

* `user_id` (int64): The id of the user to notify. Provide `user_id`, `username` or `group_id`.
* `notify_on_copy` (boolean): If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
* `notify_on_delete` (boolean): Trigger on files deleted in this path?
* `notify_on_download` (boolean): Trigger on files downloaded in this path?
* `notify_on_move` (boolean): Trigger on files moved to this path?
* `notify_on_upload` (boolean): Trigger on files created/uploaded/updated/changed in this path?
* `notify_user_actions` (boolean): If `true` actions initiated by the user will still result in a notification
* `recursive` (boolean): If `true`, enable notifications for each subfolder in this path
* `send_interval` (string): The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
* `message` (string): Custom message to include in notification emails
* `triggering_filenames` (array(string)): Array of filenames (possibly with wildcards) to scope trigger
* `triggering_group_ids` (array(int64)): If set, will only notify on actions made by a member of one of the specified groups
* `triggering_user_ids` (array(int64)): If set, will onlynotify on actions made one of the specified users
* `trigger_by_share_recipients` (boolean): Notify when actions are performed by a share recipient?
* `group_id` (int64): The ID of the group to notify.  Provide `user_id`, `username` or `group_id`.
* `path` (string): Path
* `username` (string): The username of the user to notify.  Provide `user_id`, `username` or `group_id`.


---

## Update Notification

```
files_sdk.notification.update(id, {
  "notify_on_copy": True,
  "notify_on_delete": True,
  "notify_on_download": True,
  "notify_on_move": True,
  "notify_on_upload": True,
  "notify_user_actions": True,
  "recursive": True,
  "send_interval": "daily",
  "message": "custom notification email message",
  "triggering_filenames": ["*.jpg","notify_file.txt"],
  "triggering_group_ids": [1],
  "triggering_user_ids": [1],
  "trigger_by_share_recipients": True
})
```

### Parameters

* `id` (int64): Required - Notification ID.
* `notify_on_copy` (boolean): If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
* `notify_on_delete` (boolean): Trigger on files deleted in this path?
* `notify_on_download` (boolean): Trigger on files downloaded in this path?
* `notify_on_move` (boolean): Trigger on files moved to this path?
* `notify_on_upload` (boolean): Trigger on files created/uploaded/updated/changed in this path?
* `notify_user_actions` (boolean): If `true` actions initiated by the user will still result in a notification
* `recursive` (boolean): If `true`, enable notifications for each subfolder in this path
* `send_interval` (string): The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
* `message` (string): Custom message to include in notification emails
* `triggering_filenames` (array(string)): Array of filenames (possibly with wildcards) to scope trigger
* `triggering_group_ids` (array(int64)): If set, will only notify on actions made by a member of one of the specified groups
* `triggering_user_ids` (array(int64)): If set, will onlynotify on actions made one of the specified users
* `trigger_by_share_recipients` (boolean): Notify when actions are performed by a share recipient?


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
notification = files_sdk.notification.find(id)
notification.update({
  "notify_on_copy": True,
  "notify_on_delete": True,
  "notify_on_download": True,
  "notify_on_move": True,
  "notify_on_upload": True,
  "notify_user_actions": True,
  "recursive": True,
  "send_interval": "daily",
  "message": "custom notification email message",
  "triggering_filenames": ["*.jpg","notify_file.txt"],
  "triggering_group_ids": [1],
  "triggering_user_ids": [1],
  "trigger_by_share_recipients": True
})
```

### Parameters

* `id` (int64): Required - Notification ID.
* `notify_on_copy` (boolean): If `true`, copying or moving resources into this path will trigger a notification, in addition to just uploads.
* `notify_on_delete` (boolean): Trigger on files deleted in this path?
* `notify_on_download` (boolean): Trigger on files downloaded in this path?
* `notify_on_move` (boolean): Trigger on files moved to this path?
* `notify_on_upload` (boolean): Trigger on files created/uploaded/updated/changed in this path?
* `notify_user_actions` (boolean): If `true` actions initiated by the user will still result in a notification
* `recursive` (boolean): If `true`, enable notifications for each subfolder in this path
* `send_interval` (string): The time interval that notifications are aggregated by.  Can be `five_minutes`, `fifteen_minutes`, `hourly`, or `daily`.
* `message` (string): Custom message to include in notification emails
* `triggering_filenames` (array(string)): Array of filenames (possibly with wildcards) to scope trigger
* `triggering_group_ids` (array(int64)): If set, will only notify on actions made by a member of one of the specified groups
* `triggering_user_ids` (array(int64)): If set, will onlynotify on actions made one of the specified users
* `trigger_by_share_recipients` (boolean): Notify when actions are performed by a share recipient?


---

## Delete Notification

```
notification = files_sdk.notification.find(id)
notification.delete()
```

### Parameters

* `id` (int64): Required - Notification ID.

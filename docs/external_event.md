# ExternalEvent

## Example ExternalEvent Object

```
{
  "id": 1,
  "event_type": "",
  "status": "",
  "body": "",
  "created_at": "2000-01-01T01:00:00Z",
  "body_url": "",
  "folder_behavior_id": 1,
  "successful_files": 1,
  "errored_files": 1,
  "bytes_synced": 1,
  "remote_server_type": ""
}
```

* `id` (int64): Event ID
* `event_type` (string): Type of event being recorded.
* `status` (string): Status of event.
* `body` (string): Event body
* `created_at` (date-time): External event create date/time
* `body_url` (string): Link to log file.
* `folder_behavior_id` (int64): Folder Behavior ID
* `successful_files` (int64): For sync events, the number of files handled successfully.
* `errored_files` (int64): For sync events, the number of files that encountered errors.
* `bytes_synced` (int64): For sync events, the total number of bytes synced.
* `remote_server_type` (string): Associated Remote Server type, if any


---

## List External Events

```
files_sdk.external_event.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `remote_server_type`, `event_type`, `created_at`, `status`, `site_id` or `folder_behavior_id`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status` or `folder_behavior_id`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status` or `folder_behavior_id`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status` or `folder_behavior_id`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status` or `folder_behavior_id`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status` or `folder_behavior_id`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `created_at`, `event_type`, `remote_server_type`, `status` or `folder_behavior_id`.


---

## Show External Event

```
files_sdk.external_event.find(id)
```

### Parameters

* `id` (int64): Required - External Event ID.


---

## Create External Event

```
files_sdk.external_event.create({
  "status": "status",
  "body": "body"
})
```

### Parameters

* `status` (string): Required - Status of event.
* `body` (string): Required - Event body

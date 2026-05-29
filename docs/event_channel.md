# EventChannel

## Example EventChannel Object

```
{
  "id": 1,
  "name": "example",
  "description": "example",
  "enabled": True,
  "default_channel": True,
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Event Channel ID
* `name` (string): Event Channel name.
* `description` (string): Event Channel description.
* `enabled` (boolean): Whether this Event Channel can dispatch events.
* `default_channel` (boolean): Whether this Event Channel is the default destination for newly published events.
* `created_at` (date-time): Event Channel create date/time.
* `updated_at` (date-time): Event Channel update date/time.


---

## List Event Channels

```
files_sdk.event_channel.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `enabled` and `default_channel`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `enabled` and `default_channel`.


---

## Show Event Channel

```
files_sdk.event_channel.find(id)
```

### Parameters

* `id` (int64): Required - Event Channel ID.


---

## Create Event Channel

```
files_sdk.event_channel.create({
  "name": "example",
  "description": "example",
  "enabled": True,
  "default_channel": True
})
```

### Parameters

* `name` (string): Required - Event Channel name.
* `description` (string): Event Channel description.
* `enabled` (boolean): Whether this Event Channel can dispatch events.
* `default_channel` (boolean): Whether this Event Channel is the default destination for newly published events.


---

## Update Event Channel

```
files_sdk.event_channel.update(id, {
  "name": "example",
  "description": "example",
  "enabled": True,
  "default_channel": True
})
```

### Parameters

* `id` (int64): Required - Event Channel ID.
* `name` (string): Event Channel name.
* `description` (string): Event Channel description.
* `enabled` (boolean): Whether this Event Channel can dispatch events.
* `default_channel` (boolean): Whether this Event Channel is the default destination for newly published events.


---

## Delete Event Channel

```
files_sdk.event_channel.delete(id)
```

### Parameters

* `id` (int64): Required - Event Channel ID.


---

## Update Event Channel

```
event_channel = files_sdk.event_channel.find(id)
event_channel.update({
  "name": "example",
  "description": "example",
  "enabled": True,
  "default_channel": True
})
```

### Parameters

* `id` (int64): Required - Event Channel ID.
* `name` (string): Event Channel name.
* `description` (string): Event Channel description.
* `enabled` (boolean): Whether this Event Channel can dispatch events.
* `default_channel` (boolean): Whether this Event Channel is the default destination for newly published events.


---

## Delete Event Channel

```
event_channel = files_sdk.event_channel.find(id)
event_channel.delete()
```

### Parameters

* `id` (int64): Required - Event Channel ID.

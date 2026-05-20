# UserSecurityEvent

## Example UserSecurityEvent Object

```
{
  "id": 1,
  "event_type": "example",
  "body": "example",
  "event_errors": [
    "example"
  ],
  "created_at": "2000-01-01T01:00:00Z",
  "body_url": "example",
  "user_id": 1
}
```

* `id` (int64): Event ID
* `event_type` (string): Type of user security event being recorded.
* `body` (string): Event body.
* `event_errors` (array(string)): Event errors.
* `created_at` (date-time): Event create date/time.
* `body_url` (string): Link to log file.
* `user_id` (int64): User ID.


---

## List User Security Events

```
files_sdk.user_security_event.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at` and `user_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at` and `user_id`. Valid field combinations are `[ user_id, created_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.


---

## Show User Security Event

```
files_sdk.user_security_event.find(id)
```

### Parameters

* `id` (int64): Required - User Security Event ID.

# SsoEvent

## Example SsoEvent Object

```
{
  "id": 1,
  "event_type": "example",
  "status": "example",
  "body": "example",
  "event_errors": [
    "example"
  ],
  "created_at": "2000-01-01T01:00:00Z",
  "body_url": "example",
  "user_id": 1,
  "username": "example",
  "idp_uid": "example",
  "provider": "example",
  "provider_label": "example",
  "ip": "example",
  "region": "example"
}
```

* `id` (int64): Event ID
* `event_type` (string): Type of SSO event being recorded.
* `status` (string): Status of event.
* `body` (string): Event body.
* `event_errors` (array(string)): Event errors.
* `created_at` (date-time): Event create date/time.
* `body_url` (string): Link to log file.
* `user_id` (int64): User ID.
* `username` (string): Username on Files.com for the SSO login attempt.
* `idp_uid` (string): Identity Provider UID for the SSO login attempt.
* `provider` (string): SSO provider for the SSO login attempt.
* `provider_label` (string): SSO provider label for the SSO login attempt.
* `ip` (string): IP address for the SSO login attempt.
* `region` (string): Region for the SSO login attempt.


---

## List SSO Events

```
files_sdk.sso_event.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction. Valid fields are `created_at`, `event_type`, `status` or `user_id`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`, `event_type`, `idp_uid`, `ip`, `provider`, `status`, `user_id` or `username`. Valid field combinations are `[ event_type, created_at ]`, `[ idp_uid, created_at ]`, `[ ip, created_at ]`, `[ provider, created_at ]`, `[ status, created_at ]`, `[ user_id, created_at ]`, `[ username, created_at ]`, `[ event_type, status ]`, `[ idp_uid, status ]`, `[ ip, status ]`, `[ provider, status ]`, `[ user_id, status ]`, `[ username, status ]`, `[ event_type, status, created_at ]`, `[ idp_uid, status, created_at ]`, `[ ip, status, created_at ]`, `[ provider, status, created_at ]`, `[ user_id, status, created_at ]` or `[ username, status, created_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `idp_uid`, `ip`, `provider` or `username`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.


---

## Show SSO Event

```
files_sdk.sso_event.find(id)
```

### Parameters

* `id` (int64): Required - Sso Event ID.

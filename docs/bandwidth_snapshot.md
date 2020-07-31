# BandwidthSnapshot

## Example BandwidthSnapshot Object

```
{
  "id": 1,
  "bytes_received": 1.0,
  "bytes_sent": 1.0,
  "requests_get": 1.0,
  "requests_put": 1.0,
  "requests_other": 1.0,
  "logged_at": "2000-01-01T01:00:00Z",
  "created_at": "2000-01-01T01:00:00Z",
  "updated_at": "2000-01-01T01:00:00Z"
}
```

* `id` (int64): Site bandwidth ID
* `bytes_received` (double): Site bandwidth report bytes received
* `bytes_sent` (double): Site bandwidth report bytes sent
* `requests_get` (double): Site bandwidth report get requests
* `requests_put` (double): Site bandwidth report put requests
* `requests_other` (double): Site bandwidth report other requests
* `logged_at` (date-time): Time the site bandwidth report was logged
* `created_at` (date-time): Site bandwidth report created at date/time
* `updated_at` (date-time): The last time this site bandwidth report was updated


---

## List Bandwidth Snapshots

```
files_sdk.bandwidth_snapshot.list({
  "page": 1,
  "per_page": 1
})
```

### Parameters

* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.

# PublicHostingRequestLog

## Example PublicHostingRequestLog Object

```
{
  "timestamp": "2000-01-01T01:00:00Z",
  "remote_ip": "example",
  "server_ip": "example",
  "hostname": "example",
  "path": "example",
  "responseCode": 1,
  "success": True,
  "duration_ms": 1
}
```

* `timestamp` (date-time): Start Time of Action
* `remote_ip` (string): IP Address of Public Hosting Client
* `server_ip` (string): IP Address of Public Hosting Server
* `hostname` (string): HTTP Request Hostname
* `path` (string): HTTP Request Path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `responseCode` (int64): HTTP Response Code
* `success` (boolean): Whether SFTP Action was successful.
* `duration_ms` (int64): Duration (in milliseconds)


---

## List Public Hosting Request Logs

```
files_sdk.public_hosting_request_log.list({
  "per_page": 1,
  "page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `start_date`, `end_date`, `path`, `remote_ip` or `success`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ path ]`, `[ remote_ip ]`, `[ success ]`, `[ start_date, end_date ]`, `[ start_date, path ]`, `[ start_date, remote_ip ]`, `[ start_date, success ]`, `[ end_date, path ]`, `[ end_date, remote_ip ]`, `[ end_date, success ]`, `[ path, remote_ip ]`, `[ path, success ]`, `[ remote_ip, success ]`, `[ start_date, end_date, path ]`, `[ start_date, end_date, remote_ip ]`, `[ start_date, end_date, success ]`, `[ start_date, path, remote_ip ]`, `[ start_date, path, success ]`, `[ start_date, remote_ip, success ]`, `[ end_date, path, remote_ip ]`, `[ end_date, path, success ]`, `[ end_date, remote_ip, success ]`, `[ path, remote_ip, success ]`, `[ start_date, end_date, path, remote_ip ]`, `[ start_date, end_date, path, success ]`, `[ start_date, end_date, remote_ip, success ]`, `[ start_date, path, remote_ip, success ]` or `[ end_date, path, remote_ip, success ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `path`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ path ]`, `[ remote_ip ]`, `[ success ]`, `[ start_date, end_date ]`, `[ start_date, path ]`, `[ start_date, remote_ip ]`, `[ start_date, success ]`, `[ end_date, path ]`, `[ end_date, remote_ip ]`, `[ end_date, success ]`, `[ path, remote_ip ]`, `[ path, success ]`, `[ remote_ip, success ]`, `[ start_date, end_date, path ]`, `[ start_date, end_date, remote_ip ]`, `[ start_date, end_date, success ]`, `[ start_date, path, remote_ip ]`, `[ start_date, path, success ]`, `[ start_date, remote_ip, success ]`, `[ end_date, path, remote_ip ]`, `[ end_date, path, success ]`, `[ end_date, remote_ip, success ]`, `[ path, remote_ip, success ]`, `[ start_date, end_date, path, remote_ip ]`, `[ start_date, end_date, path, success ]`, `[ start_date, end_date, remote_ip, success ]`, `[ start_date, path, remote_ip, success ]` or `[ end_date, path, remote_ip, success ]`.

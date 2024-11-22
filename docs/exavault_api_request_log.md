# ExavaultApiRequestLog

## Example ExavaultApiRequestLog Object

```
{
  "timestamp": "2000-01-01T01:00:00Z",
  "endpoint": "example",
  "version": "example",
  "request_ip": "example",
  "request_method": "example",
  "error_type": "example",
  "error_message": "example",
  "user_agent": "example",
  "response_code": 1,
  "success": True,
  "duration_ms": 1
}
```

* `timestamp` (date-time): Start Time of Action
* `endpoint` (string): Name of API Endpoint
* `version` (string): Exavault API Version
* `request_ip` (string): IP of requesting client
* `request_method` (string): HTTP Method
* `error_type` (string): Error type, if applicable
* `error_message` (string): Error message, if applicable
* `user_agent` (string): User-Agent
* `response_code` (int64): HTTP Response Code
* `success` (boolean): `false` if HTTP Response Code is 4xx or 5xx
* `duration_ms` (int64): Duration (in milliseconds)


---

## List Exavault API Request Logs

```
files_sdk.exavault_api_request_log.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `start_date`, `end_date`, `request_ip`, `request_method` or `success`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ request_ip ]`, `[ request_method ]`, `[ success ]`, `[ start_date, end_date ]`, `[ start_date, request_ip ]`, `[ start_date, request_method ]`, `[ start_date, success ]`, `[ end_date, request_ip ]`, `[ end_date, request_method ]`, `[ end_date, success ]`, `[ request_ip, request_method ]`, `[ request_ip, success ]`, `[ request_method, success ]`, `[ start_date, end_date, request_ip ]`, `[ start_date, end_date, request_method ]`, `[ start_date, end_date, success ]`, `[ start_date, request_ip, request_method ]`, `[ start_date, request_ip, success ]`, `[ start_date, request_method, success ]`, `[ end_date, request_ip, request_method ]`, `[ end_date, request_ip, success ]`, `[ end_date, request_method, success ]`, `[ request_ip, request_method, success ]`, `[ start_date, end_date, request_ip, request_method ]`, `[ start_date, end_date, request_ip, success ]`, `[ start_date, end_date, request_method, success ]`, `[ start_date, request_ip, request_method, success ]` or `[ end_date, request_ip, request_method, success ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `request_ip` and `request_method`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ request_ip ]`, `[ request_method ]`, `[ success ]`, `[ start_date, end_date ]`, `[ start_date, request_ip ]`, `[ start_date, request_method ]`, `[ start_date, success ]`, `[ end_date, request_ip ]`, `[ end_date, request_method ]`, `[ end_date, success ]`, `[ request_ip, request_method ]`, `[ request_ip, success ]`, `[ request_method, success ]`, `[ start_date, end_date, request_ip ]`, `[ start_date, end_date, request_method ]`, `[ start_date, end_date, success ]`, `[ start_date, request_ip, request_method ]`, `[ start_date, request_ip, success ]`, `[ start_date, request_method, success ]`, `[ end_date, request_ip, request_method ]`, `[ end_date, request_ip, success ]`, `[ end_date, request_method, success ]`, `[ request_ip, request_method, success ]`, `[ start_date, end_date, request_ip, request_method ]`, `[ start_date, end_date, request_ip, success ]`, `[ start_date, end_date, request_method, success ]`, `[ start_date, request_ip, request_method, success ]` or `[ end_date, request_ip, request_method, success ]`.


---

## Create an export CSV of Exavault API Request Log resources

```
files_sdk.exavault_api_request_log.create_export()
```

### Parameters

* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `start_date`, `end_date`, `request_ip`, `request_method` or `success`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ request_ip ]`, `[ request_method ]`, `[ success ]`, `[ start_date, end_date ]`, `[ start_date, request_ip ]`, `[ start_date, request_method ]`, `[ start_date, success ]`, `[ end_date, request_ip ]`, `[ end_date, request_method ]`, `[ end_date, success ]`, `[ request_ip, request_method ]`, `[ request_ip, success ]`, `[ request_method, success ]`, `[ start_date, end_date, request_ip ]`, `[ start_date, end_date, request_method ]`, `[ start_date, end_date, success ]`, `[ start_date, request_ip, request_method ]`, `[ start_date, request_ip, success ]`, `[ start_date, request_method, success ]`, `[ end_date, request_ip, request_method ]`, `[ end_date, request_ip, success ]`, `[ end_date, request_method, success ]`, `[ request_ip, request_method, success ]`, `[ start_date, end_date, request_ip, request_method ]`, `[ start_date, end_date, request_ip, success ]`, `[ start_date, end_date, request_method, success ]`, `[ start_date, request_ip, request_method, success ]` or `[ end_date, request_ip, request_method, success ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `request_ip` and `request_method`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ request_ip ]`, `[ request_method ]`, `[ success ]`, `[ start_date, end_date ]`, `[ start_date, request_ip ]`, `[ start_date, request_method ]`, `[ start_date, success ]`, `[ end_date, request_ip ]`, `[ end_date, request_method ]`, `[ end_date, success ]`, `[ request_ip, request_method ]`, `[ request_ip, success ]`, `[ request_method, success ]`, `[ start_date, end_date, request_ip ]`, `[ start_date, end_date, request_method ]`, `[ start_date, end_date, success ]`, `[ start_date, request_ip, request_method ]`, `[ start_date, request_ip, success ]`, `[ start_date, request_method, success ]`, `[ end_date, request_ip, request_method ]`, `[ end_date, request_ip, success ]`, `[ end_date, request_method, success ]`, `[ request_ip, request_method, success ]`, `[ start_date, end_date, request_ip, request_method ]`, `[ start_date, end_date, request_ip, success ]`, `[ start_date, end_date, request_method, success ]`, `[ start_date, request_ip, request_method, success ]` or `[ end_date, request_ip, request_method, success ]`.

# EmailLog

## Example EmailLog Object

```
{
  "timestamp": "2000-01-01T01:00:00Z",
  "message": "example",
  "status": "example",
  "subject": "example",
  "to": "example",
  "cc": "example"
}
```

* `timestamp` (date-time): Start Time of Action
* `message` (string): Log Message
* `status` (string): Status of E-Mail delivery
* `subject` (string): Subject line of E-Mail
* `to` (string): To field of E-Mail
* `cc` (string): CC field of E-Mail


---

## List Email Logs

```
files_sdk.email_log.list({
  "per_page": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `start_date`, `end_date` or `status`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ status ]`, `[ start_date, end_date ]`, `[ start_date, status ]` or `[ end_date, status ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `status`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ status ]`, `[ start_date, end_date ]`, `[ start_date, status ]` or `[ end_date, status ]`.

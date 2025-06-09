# EmailLog

## Example EmailLog Object

```
{
  "timestamp": "2000-01-01T01:00:00Z",
  "message": "example",
  "status": "example",
  "subject": "example",
  "to": "example",
  "cc": "example",
  "delivery_method": "example",
  "smtp_hostname": "example",
  "smtp_ip": "example",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `timestamp` (date-time): Start Time of Action. Deprecrated: Use created_at.
* `message` (string): Log Message
* `status` (string): Status of E-Mail delivery
* `subject` (string): Subject line of E-Mail
* `to` (string): To field of E-Mail
* `cc` (string): CC field of E-Mail
* `delivery_method` (string): How was the email delivered?  `customer_smtp` or `files.com`
* `smtp_hostname` (string): Customer SMTP Hostname used.
* `smtp_ip` (string): Customer SMTP IP address as resolved for use (useful for troubleshooting DNS issues with customer SMTP).
* `created_at` (date-time): Start Time of Action


---

## List Email Logs

```
files_sdk.email_log.list()
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `start_date`, `end_date`, `status` or `created_at`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ status ]`, `[ created_at ]`, `[ start_date, end_date ]`, `[ start_date, status ]`, `[ start_date, created_at ]`, `[ end_date, status ]`, `[ end_date, created_at ]`, `[ status, created_at ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, created_at ]`, `[ start_date, status, created_at ]` or `[ end_date, status, created_at ]`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ status ]`, `[ created_at ]`, `[ start_date, end_date ]`, `[ start_date, status ]`, `[ start_date, created_at ]`, `[ end_date, status ]`, `[ end_date, created_at ]`, `[ status, created_at ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, created_at ]`, `[ start_date, status, created_at ]` or `[ end_date, status, created_at ]`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ status ]`, `[ created_at ]`, `[ start_date, end_date ]`, `[ start_date, status ]`, `[ start_date, created_at ]`, `[ end_date, status ]`, `[ end_date, created_at ]`, `[ status, created_at ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, created_at ]`, `[ start_date, status, created_at ]` or `[ end_date, status, created_at ]`.
* `filter_prefix` (object): If set, return records where the specified field is prefixed by the supplied value. Valid fields are `status`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ status ]`, `[ created_at ]`, `[ start_date, end_date ]`, `[ start_date, status ]`, `[ start_date, created_at ]`, `[ end_date, status ]`, `[ end_date, created_at ]`, `[ status, created_at ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, created_at ]`, `[ start_date, status, created_at ]` or `[ end_date, status, created_at ]`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ status ]`, `[ created_at ]`, `[ start_date, end_date ]`, `[ start_date, status ]`, `[ start_date, created_at ]`, `[ end_date, status ]`, `[ end_date, created_at ]`, `[ status, created_at ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, created_at ]`, `[ start_date, status, created_at ]` or `[ end_date, status, created_at ]`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`. Valid field combinations are `[ start_date ]`, `[ end_date ]`, `[ status ]`, `[ created_at ]`, `[ start_date, end_date ]`, `[ start_date, status ]`, `[ start_date, created_at ]`, `[ end_date, status ]`, `[ end_date, created_at ]`, `[ status, created_at ]`, `[ start_date, end_date, status ]`, `[ start_date, end_date, created_at ]`, `[ start_date, status, created_at ]` or `[ end_date, status, created_at ]`.

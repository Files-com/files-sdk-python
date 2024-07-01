# InboxUpload

## Example InboxUpload Object

```
{
  "inbox_registration": "example",
  "path": "a/b/test.txt",
  "created_at": "2000-01-01T01:00:00Z"
}
```

* `inbox_registration` (InboxRegistration): 
* `path` (string): Upload path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `created_at` (date-time): Upload date/time


---

## List Inbox Uploads

```
files_sdk.inbox_upload.list({
  "per_page": 1,
  "page": 1,
  "inbox_registration_id": 1,
  "inbox_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  When a list request has more records available, cursors are provided in the response headers `X-Files-Cursor-Next` and `X-Files-Cursor-Prev`.  Send one of those cursor value here to resume an existing list from the next available record.  Note: many of our SDKs have iterator methods that will automatically handle cursor-based pagination.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): 
* `page` (int64): 
* `sort_by` (object): If set, sort records by the specified field in either `asc` or `desc` direction (e.g. `sort_by[created_at]=desc`). Valid fields are `created_at`.
* `filter` (object): If set, return records where the specified field is equal to the supplied value. Valid fields are `created_at`.
* `filter_gt` (object): If set, return records where the specified field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specified field is greater than or equal the supplied value. Valid fields are `created_at`.
* `filter_lt` (object): If set, return records where the specified field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specified field is less than or equal the supplied value. Valid fields are `created_at`.
* `inbox_registration_id` (int64): InboxRegistration ID
* `inbox_id` (int64): Inbox ID

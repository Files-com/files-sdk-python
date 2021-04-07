# InboxUpload

## Example InboxUpload Object

```
{
  "inbox_registration": "",
  "path": "a/b/test.txt",
  "created_at": "2020-01-01 00:00:00"
}
```

* `inbox_registration`: 
* `path` (string): Upload path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `created_at` (date-time): Upload date/time


---

## List Inbox Uploads

```
files_sdk.inbox_upload.list({
  "per_page": 1,
  "inbox_registration_id": 1,
  "inbox_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `sort_by` (object): If set, sort records by the specified field in either 'asc' or 'desc' direction (e.g. sort_by[last_login_at]=desc). Valid fields are `created_at`.
* `filter` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `created_at`.
* `filter_gt` (object): If set, return records where the specifiied field is greater than the supplied value. Valid fields are `created_at`.
* `filter_gteq` (object): If set, return records where the specifiied field is greater than or equal to the supplied value. Valid fields are `created_at`.
* `filter_like` (object): If set, return records where the specifiied field is equal to the supplied value. Valid fields are `created_at`.
* `filter_lt` (object): If set, return records where the specifiied field is less than the supplied value. Valid fields are `created_at`.
* `filter_lteq` (object): If set, return records where the specifiied field is less than or equal to the supplied value. Valid fields are `created_at`.
* `inbox_registration_id` (int64): InboxRegistration ID
* `inbox_id` (int64): Inbox ID

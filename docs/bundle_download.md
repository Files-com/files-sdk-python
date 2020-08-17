# BundleDownload

## Example BundleDownload Object

```
{
  "download_method": "file",
  "path": "a/b/test.txt",
  "created_at": "2020-01-01 00:00:00"
}
```

* `download_method` (string): Download method (file or full_zip)
* `path` (string): Download path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `created_at` (date-time): Download date/time


---

## List Bundle Downloads

```
files_sdk.bundle_download.list({
  "page": 1,
  "per_page": 1,
  "bundle_registration_id": 1
})
```

### Parameters

* `page` (int64): Current page number.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `action` (string): Deprecated: If set to `count` returns a count of matching records rather than the records themselves.
* `cursor` (string): Send cursor to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `bundle_registration_id` (int64): Required - BundleRegistration ID

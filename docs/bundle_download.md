# BundleDownload

## Example BundleDownload Object

```
{
  "bundle_registration": "",
  "download_method": "file",
  "path": "a/b/test.txt",
  "created_at": "2020-01-01 00:00:00"
}
```

* `bundle_registration`: 
* `download_method` (string): Download method (file or full_zip)
* `path` (string): Download path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `created_at` (date-time): Download date/time


---

## List Bundle Downloads

```
files_sdk.bundle_download.list({
  "per_page": 1,
  "bundle_id": 1,
  "bundle_registration_id": 1
})
```

### Parameters

* `cursor` (string): Used for pagination.  Send a cursor value to resume an existing list from the point at which you left off.  Get a cursor from an existing list via the X-Files-Cursor-Next header.
* `per_page` (int64): Number of records to show per page.  (Max: 10,000, 1,000 or less is recommended).
* `bundle_id` (int64): Bundle ID
* `bundle_registration_id` (int64): BundleRegistration ID

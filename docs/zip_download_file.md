# ZipDownloadFile

## Example ZipDownloadFile Object

```
{
  "site_id": 1,
  "user_id": 1,
  "bundle_id": 1,
  "bundle_registration_id": 1,
  "files": [
    "example"
  ],
  "cursor": "example"
}
```

* `site_id` (int64): Site Id
* `user_id` (int64): User Id
* `bundle_id` (int64): Bundle Id
* `bundle_registration_id` (int64): Bundle Registration Id
* `files` (array(object)): A list of file names, sizes, and signed download URLs.
* `cursor` (string): Cursor for fetching more files in subsequent requests.
* `code` (string): Secure code that was generated when creating the zip download.
* `limit` (int64): Limit the number of files returned.


---

## Fetch a set of file resources for a ZIP: POST /zip_download_files

```
files_sdk.zip_download_file.create({
  "code": "code",
  "limit": 1,
  "site_id": 1
})
```

### Parameters

* `code` (string): Required - Secure code that was generated when creating the zip download.
* `limit` (int64): Limit the number of files returned.
* `cursor` (string): Cursor used for paging through files.
* `site_id` (int64): Only check the given site for the zip download.

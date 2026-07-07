# ZipDownloadFiles

## Example ZipDownloadFiles Object

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

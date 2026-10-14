# BundlePath

## Example BundlePath Object

The API sends each `BundlePath` record as JSON, such as:

```json
{
  "recursive": true,
  "path": "example"
}
```

* `recursive` (boolean): Allow access to subfolders content?
* `path` (string): The path to the resource relative to filesystem. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.

# ZipListEntry

## Example ZipListEntry Object

The API sends each `ZipListEntry` record as JSON, such as:

```json
{
  "path": "example",
  "size": 1
}
```

* `path` (string): Entry path inside the ZIP. This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `size` (int64): Uncompressed size in bytes.

# FilePartUpload

## Example FilePartUpload Object

```
{
  "send": "",
  "action": "upload/direct",
  "ask_about_overwrites": True,
  "available_parts": 1,
  "expires": "",
  "headers": "",
  "http_method": "POST",
  "next_partsize": 1,
  "parallel_parts": True,
  "parameters": "{}",
  "part_number": 1,
  "partsize": 1,
  "path": "",
  "ref": "upload-1",
  "upload_uri": ""
}
```

* `send` (object): Content-Type and File to send
* `action` (string): Type of upload
* `ask_about_overwrites` (boolean): If false, rename conflicting files instead of asking for overwrite confirmation
* `available_parts` (int64): Currently unused
* `expires` (string): Currently unused
* `headers` (object): Additional upload headers
* `http_method` (string): Upload method, usually POST
* `next_partsize` (int64): Currently unused
* `parallel_parts` (boolean): If true, parts may be uploaded in parallel
* `parameters` (object): Additional upload parameters
* `part_number` (int64): Currently unused
* `partsize` (int64): Currently unused
* `path` (string): Upload path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `ref` (string): Reference name for this upload part
* `upload_uri` (string): URI to upload this part to

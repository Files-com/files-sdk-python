# FilePartUpload

## Example FilePartUpload Object

```
{
  "send": "",
  "action": "upload/direct",
  "ask_about_overwrites": True,
  "available_parts": "",
  "expires": "",
  "headers": "",
  "http_method": "POST",
  "next_partsize": "",
  "parameters": "",
  "part_number": "",
  "partsize": "",
  "path": "",
  "ref": "upload-1",
  "upload_uri": ""
}
```

* `send` (object): Content-Type and File to send
* `action` (string): Type of upload
* `ask_about_overwrites` (boolean): If false, rename conflicting files instead of asking for overwrite confirmation
* `available_parts` (string): Currently unused
* `expires` (string): Currently unused
* `headers` (object): Additional upload headers
* `http_method` (string): Upload method, usually POST
* `next_partsize` (string): Currently unused
* `parameters` (string): Additional upload parameters
* `part_number` (string): Currently unused
* `partsize` (string): Currently unused
* `path` (string): Upload path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `ref` (string): Reference name for this upload part
* `upload_uri` (string): URI to upload this part to

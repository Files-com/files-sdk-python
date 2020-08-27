# FileUploadPart

## Example FileUploadPart Object

```
{
  "send": "",
  "action": "multipart",
  "ask_about_overwrites": True,
  "available_parts": 1,
  "expires": "",
  "headers": "",
  "http_method": "PUT",
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
* `ask_about_overwrites` (boolean): If `true`, this file exists and you may wish to ask the user for overwrite confirmation
* `available_parts` (int64): Number of parts in the upload
* `expires` (string): Date/time of when this Upload part expires and the URL cannot be used any more
* `headers` (object): Additional upload headers to provide as part of the upload
* `http_method` (string): HTTP Method to use for uploading the part, usually `PUT`
* `next_partsize` (int64): Size in bytes for this part
* `parallel_parts` (boolean): If `true`, multiple parts may be uploaded in parallel.  If `false`, be sure to only upload one part at a time, in order.
* `parameters` (object): Additional HTTP parameters to send with the upload
* `part_number` (int64): Number of this upload part
* `partsize` (int64): Size in bytes for the next upload part
* `path` (string): New file path This must be slash-delimited, but it must neither start nor end with a slash. Maximum of 5000 characters.
* `ref` (string): Reference name for this upload part
* `upload_uri` (string): URI to upload this part to

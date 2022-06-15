# Preview

## Example Preview Object

```
{
  "id": 1,
  "status": "complete",
  "download_uri": "https://mysite.files.com/...",
  "type": "image",
  "size": "large"
}
```

* `id` (int64): Preview ID
* `status` (string): Preview status.  Can be invalid, not_generated, generating, complete, or file_too_large
* `download_uri` (string): Link to download preview
* `type` (string): Preview type. Can be image, pdf, pdf_native, video, or audio
* `size` (string): Preview size

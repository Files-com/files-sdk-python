# Preview

## Example Preview Object

```
{
  "id": 1,
  "status": "complete",
  "download_uri": "https://mysite.files.com/...",
  "type": "complete",
  "size": 1024
}
```

* `id` (int64): Preview ID
* `status` (string): Preview status.  Can be invalid, not_generated, generating, complete, or file_too_large
* `download_uri` (string): Link to download preview
* `type` (string): Preview status.  Can be invalid, not_generated, generating, complete, or file_too_large
* `size` (int64): Preview size
